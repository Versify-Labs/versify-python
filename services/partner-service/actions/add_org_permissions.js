/**
* Handler that will be called during the execution of a PostLogin flow.
*
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
*/
exports.onExecutePostLogin = async (event, api) => {
    const namespace = 'https://versifylabs.com';
    const userId = event.user.user_id

    const ManagementClient = require('auth0').ManagementClient;
    const management = new ManagementClient({
        domain: event.secrets.domain,
        clientId: event.secrets.clientId,
        clientSecret: event.secrets.clientSecret,
    });

    // Construct
    let result = {
        users_organizations: [],
        users_organizations_roles: [],
        all_roles: []
    }

    // Get permissions
    let perms = []
    let permCount = 0
    let organizations = await management.users.getUserOrganizations({ id: userId })
    result.users_organizations = organizations
    organizations.forEach(async (org) => {
        let userOrgRoles = await management.organizations.getMemberRoles({ id: org.id, user_id: userId })
        userOrgRoles.forEach(async (role) => {
            let rolePerms = await management.roles.getPermissions({ id: role.id })
            rolePerms.forEach((perm) => {
                console.log(`Adding perm: ${org.id}:${perm.permission_name}`)
                perms.push(`${org.id}:${perm.permission_name}`)
                permCount += 1
                console.log('Total Permissions: ' + permCount)
            })
        })
    })
    console.log('Result:')
    console.log(result)

    // Update claims
    api.accessToken.setCustomClaim(`${namespace}/permissions`, result);
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
