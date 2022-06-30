/**
* Handler that will be called during the execution of a PostLogin flow.
*
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
*/
exports.onExecutePostLogin = async (event, api) => {
    console.log(event)

    const namespace = 'https://versifylabs.com';
    const userId = event.user.user_id

    const ManagementClient = require('auth0').ManagementClient;
    const management = new ManagementClient({
        domain: event.secrets.domain,
        clientId: event.secrets.clientId,
        clientSecret: event.secrets.clientSecret,
    });

    // Get permissions
    let perms = []
    event.user.user_id
    let userPermissions = await management.getUserPermissions({ id: userId })
    userPermissions.forEach((perm) => {
        perms.push(`${userId}:${perm.permission_name}`)
    })
    console.log('All Permissions:')
    console.log(perms)

    // Update custom claims
    api.accessToken.setCustomClaim(`${namespace}/permissions`, perms);
    if (event.authorization) {
        api.idToken.setCustomClaim(`${namespace}/email`, event.user.email);
        api.accessToken.setCustomClaim(`${namespace}/email`, event.user.email);
        api.idToken.setCustomClaim(`${namespace}/roles`, event.authorization.roles);
        api.accessToken.setCustomClaim(`${namespace}/roles`, event.authorization.roles);
    }
    if (event.organization) {
        api.idToken.setCustomClaim(`${namespace}/organization`, event.organization);
        api.accessToken.setCustomClaim(`${namespace}/organization`, event.organization);
    }
};

/**
* Handler that will be invoked when this action is resuming after an external redirect. If your
* onExecutePostLogin function does not perform a redirect, this function can be safely ignored.
*
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
*/
  // exports.onContinuePostLogin = async (event, api) => {
  // };
