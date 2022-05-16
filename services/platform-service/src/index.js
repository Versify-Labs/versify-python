const { Magic } = require("@magic-sdk/admin");
const SecretsManager = require('./secrets.js');

const getMetadata = async (DIDToken) => {
    const secretName = process.env.SECRET_NAME;
    const region = process.env.AWS_REGION;
    const data = await SecretsManager.getSecret(secretName, region);
    const value = JSON.parse(data);
    const magicSecretKey = value['MAGIC_SK']
    const magic = new Magic(magicSecretKey);
    try {
        magic.token.validate(DIDToken);
        console.log('Authorized')
    } catch (error) {
        console.error('Invalid token')
        return callback('Invalid token');
    }
    const metadata = await magic.users.getMetadataByToken(DIDToken);
    return metadata
};

const generatePolicy = (principalId, effect, resource, metadata = {}) => {
    const authResponse = {};
    authResponse.principalId = principalId;
    if (effect && resource) {
        const statementOne = {};
        statementOne.Action = 'execute-api:Invoke';
        statementOne.Effect = effect;
        statementOne.Resource = resource;
        const policyDocument = {};
        policyDocument.Version = '2012-10-17';
        policyDocument.Statement = [statementOne];
        authResponse.policyDocument = policyDocument;
    }
    authResponse.context = {
        'success': true,
        'email': metadata.email,
        'issuer': metadata.issuer,
        'oauthProvider': metadata.oauthProvider,
        'phoneNumber': metadata.phoneNumber,
        'publicAddress': metadata.publicAddress,
    }
    console.log(authResponse)
    return authResponse;
};

exports.handler = (event, context, callback) => {
    let authorization = event.headers.Authorization || event.headers.authorization
    if (!authorization) {
        return callback('Missing token');
    }
    const tokenParts = authorization.split(' ');
    const DIDToken = tokenParts[1];
    if (!(tokenParts[0].toLowerCase() === 'bearer' && DIDToken)) {
        return callback('Missing token');
    }
    getMetadata(DIDToken).then((metadata) => {
        callback(null, generatePolicy(metadata.email, 'Allow', event.methodArn, metadata))
    }).catch('error', (e) => {
        callback(Error(e))
    })
};
