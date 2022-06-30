/**
* Handler that will be called during the execution of a PostLogin flow.
*
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
*/
exports.onExecutePostLogin = async (event, api) => {
    const namespace = 'https://versifylabs.com';
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