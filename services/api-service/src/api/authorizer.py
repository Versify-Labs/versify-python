from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    DENY_ALL_RESPONSE, APIGatewayAuthorizerRequestEvent,
    APIGatewayAuthorizerResponse)
from jose import jwt

from ..utils.stytch import stytch
from .resources import Versify

logger = Logger()


def get_user_by_token(token):
    if not token:
        return

    claims = jwt.get_unverified_claims(token)
    logger.info({'claims': claims})
    if not claims:
        return

    session = claims.get('https://stytch.com/session')
    if not session:
        return

    stytch_user_id = claims.get('sub')
    if not stytch_user_id:
        return

    # Build user object
    auth_factors = session.get('authentication_factors', [])
    user_body = {'stytch_user': stytch_user_id}
    for factor in auth_factors:

        # Handle Magic Link session
        if factor.get('type') == 'magic_link':
            email_factor = factor.get('email_factor', {})
            user_body['email'] = email_factor.get('email_address')

        # Handle Oauth session
        if factor.get('type') == 'oauth':
            user = stytch().get_user(stytch_user_id)
            logger.info(user)

            # user_body['avatar'] = user['providers'][0]['profile_picture_url']
            user_body['email'] = user['emails'][0]['email']
            user_body['first_name'] = user['name'].get('first_name')
            user_body['last_name'] = user['name'].get('last_name')
            user_body['wallets'] = user['crypto_wallets']

    user = Versify().user.create(user_body)
    logger.info({'Created/updated User': user})

    return user


def generate_authenticated_response(arn, account=None, email=None, user=None):
    context = {
        'account': account,
        'email': email,
        'user': user
    }
    policy = APIGatewayAuthorizerResponse(
        principal_id=user or 'Unkown',
        context=context,
        region=arn.region,
        aws_account_id=arn.aws_account_id,
        api_id=arn.api_id,
        stage=arn.stage,
    )
    policy.allow_all_routes()
    result = policy.asdict()
    return result


def handle_key(arn, key, account_id=None):
    # Validate that the key belongs to the account
    account = Versify().account.get(filter={'account': account_id})
    if account['settings']['auth'].get('api_secret_key') == key:
        return generate_authenticated_response(arn, account_id)
    return DENY_ALL_RESPONSE


def handle_token(arn, token, account_id=None):

    # Lookup user making the request by the email
    user = get_user_by_token(token)
    if not user:
        logger.error('Invalid user')
        return DENY_ALL_RESPONSE

    # If account data is being requested, we need to validate
    if account_id:

        # Confirm the user has access to the requested request
        has_access = False
        for user_account in user.get('accounts', []):
            if user_account['id'] == account_id:
                has_access = True
                break
        if not has_access:
            logger.error('Access denied for account ' + account_id)
            return DENY_ALL_RESPONSE

    email = user['email']
    user_id = user['id']
    return generate_authenticated_response(arn, account_id, email, user_id)


@event_source(data_class=APIGatewayAuthorizerRequestEvent)  # type: ignore
def handler(event: APIGatewayAuthorizerRequestEvent, context):

    # Parse the `methodArn` as an `APIGatewayRouteArn`
    arn = event.parsed_arn

    # Parse Auth Data
    auth = event.get_header_value('authorization')
    account_id = event.get_header_value('versify-account')
    token_type, token = auth.split(' ') if auth else 'ERROR ERROR'
    api_key = None
    auth_token = None
    if token_type.lower() == 'basic':
        api_key = token
    elif token_type.lower() == 'bearer':
        auth_token = token
    logger.info({
        'account': account_id,
        'api_key': api_key,
        'auth_token': auth_token,
    })

    if api_key:
        return handle_key(arn, api_key, account_id)

    if auth_token:
        return handle_token(arn, auth_token, account_id)
