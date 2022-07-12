/**
* Handler that will be called during the execution of a PostLogin flow.
*
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
*/
exports.onExecutePostLogin = async (event, api) => {
    const namespace = 'https://versifylabs.com';

    if (event.authorization) {
        const ManagementClient = require('auth0').ManagementClient;
        const management = new ManagementClient({
            domain: event.secrets.AUTH0_RULES_DOMAIN,
            clientId: event.secrets.AUTH0_RULES_CLIENT_ID,
            clientSecret: event.secrets.AUTH0_RULES_CLIENT_SECRET,
        });

        api.idToken.setCustomClaim(`${namespace}/email`, event.user.email);
        api.accessToken.setCustomClaim(`${namespace}/email`, event.user.email);

        api.idToken.setCustomClaim(`${namespace}/user`, event.user.user_id);
        api.accessToken.setCustomClaim(`${namespace}/user`, event.user.user_id);

        let roles = []

        // Add user roles
        event.authorization.roles.forEach((role) => {
            // console.log(`Adding role: ${event.user.user_id}:${role}`)
            roles.push(`${event.user.user_id}:${role}`)
        })

        // Add org roles
        let organizations = await management.users.getUserOrganizations({ id: event.user.user_id })
        organizations.forEach(async (org) => {
            let userOrgRoles = await management.organizations.getMemberRoles({
                id: org.id, user_id: event.user.user_id
            })
            userOrgRoles.forEach((role) => {
                // console.log(`Adding role: ${org.id}:${role.id}`)
                roles.push(`${org.id}:${role.id}`)
            })
        })
        await new Promise(async (resolve) => {
            setTimeout(resolve, 1000);
        });

        api.idToken.setCustomClaim(`${namespace}/roles`, roles);
        api.accessToken.setCustomClaim(`${namespace}/roles`, roles);

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
