from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import (
    DENY_ALL_RESPONSE, APIGatewayAuthorizerRequestEvent,
    APIGatewayAuthorizerResponse)

from ..services import AccountService, AuthService, UserService

tracer = Tracer()
logger = Logger()

account_service = AccountService()
user_service = UserService(account_service)
auth_service = AuthService(account_service, user_service)


def generate_authenticated_response(arn, account=None, email=None, user=None):
    context = {
        'account': account,
        'email': email,
        'user': user
    }
    logger.info('Context')
    logger.info(context)
    policy = APIGatewayAuthorizerResponse(
        principal_id=user or email or account or 'Unknown',
        context=context,
        region=arn.region,
        aws_account_id=arn.aws_account_id,
        api_id=arn.api_id,
        stage=arn.stage,
    )
    policy.allow_all_routes()
    result = policy.asdict()
    logger.info(result)
    return result


@event_source(data_class=APIGatewayAuthorizerRequestEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler  # type: ignore
def authorize_account(event: APIGatewayAuthorizerRequestEvent, context):

    # Parse the `methodArn` as an `APIGatewayRouteArn`
    arn = event.parsed_arn

    # Parse authentication data
    auth = event.get_header_value(
        name='authorization',
        case_sensitive=False
    )
    account = event.get_header_value(
        name='versify-account',
        case_sensitive=False
    )
    token_type, token = auth.split(' ') if auth else 'ERROR ERROR'

    # Sanity checks
    if any([
        not account,
        not token,
        not token_type,
        token_type.lower() not in ['bearer', 'basic']
    ]):
        return DENY_ALL_RESPONSE

    # Run authorization steps
    success = False
    user = None
    error = None
    if token_type.lower() == 'basic':
        success, user, error = auth_service.authenticate_account_api_key(token)
    if token_type.lower() == 'bearer':
        success, user, error = auth_service.authenticate_account_token(
            account, token)

    if success and user:
        email = user['email']
        user_id = user['id']
        return generate_authenticated_response(arn, account, email, user_id)
    else:
        logger.error(error)
        return DENY_ALL_RESPONSE


@event_source(data_class=APIGatewayAuthorizerRequestEvent)  # type: ignore
@logger.inject_lambda_context(log_event=True)  # type: ignore
@tracer.capture_lambda_handler  # type: ignore
def authorize_user(event: APIGatewayAuthorizerRequestEvent, context):

    # Parse the `methodArn` as an `APIGatewayRouteArn`
    arn = event.parsed_arn

    # Parse authentication data
    auth = event.get_header_value(
        name='authorization',
        case_sensitive=False
    )
    token_type, token = auth.split(' ') if auth else 'ERROR ERROR'
    if not token_type or not token or token_type.lower() != 'bearer':
        logger.error('Invalid auth parameter.')
        return DENY_ALL_RESPONSE

    # Run authorization steps
    success, user, error = auth_service.authenticate_user_token(token)
    if success and user:
        logger.info(user)
        account = None
        email = user['email']
        user_id = user['id']
        return generate_authenticated_response(arn, account, email, user_id)
    else:
        logger.error(error)
        return DENY_ALL_RESPONSE
