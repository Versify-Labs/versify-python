// This rule adds the authenticated user's email address to the access token.

function addEmailToAccessToken(user, context, callback) {
    var namespace = 'https://example.com/';
    context.accessToken[namespace + 'email'] = user.email;
    return callback(null, user, context);
}