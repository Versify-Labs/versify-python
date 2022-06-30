// This rule adds standard user permissions to the access token

function addUserPermsToAccessToken(user, context, callback) {
    var namespace = 'versify';
    context.accessToken[namespace + '/perms'] = [
        'GET:/auth/v1/users/{user_id}',
        'PUT:/auth/v1/users/{user_id}',
        'GET:/auth/v1/users/{user_id}/organizations'
    ];
    return callback(null, user, context);
}