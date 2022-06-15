/**
* Handler that will be called during the execution of a PostLogin flow.
*
* @param {Event} event - Details about the user and the context in which they are logging in.
* @param {PostLoginAPI} api - Interface whose methods can be used to change the behavior of the login.
*/

exports.onExecutePostLogin = async (event, api) => {

    // Only run for organization logins
    if (event.organization) {
        let stripe_customer = '';

        if ('stripe_customer' in event.organization.metadata) {
            // Stripe customer already exists
            stripe_customer = event.organization.metadata.stripe_customer

        } else {

            const stripe = require('stripe')(event.secrets.STRIPE_SECRET_KEY);
            console.log('Stripe intialized')

            const ManagementClient = require('auth0').ManagementClient;
            const management = new ManagementClient({
                domain: event.secrets.domain,
                clientId: event.secrets.clientId,
                clientSecret: event.secrets.clientSecret,
            });
            console.log('Management API intialized')

            // Create stripe customer
            console.log('Creating stripe customer for organization')
            const customer = await stripe.customers.create({
                description: 'Organization Customer',
                email: event.user.email,
                metadata: {
                    organization: event.organization.id
                },
                name: event.organization.display_name,
            });
            console.log(customer)

            // Subscribe customer to free plan
            console.log('Subscribing stripe customer to free plan')
            const subscription = await stripe.subscriptions.create({
                customer: customer.id,
                items: [
                    { price: event.secrets.STRIPE_FREE_PLAN_PRICE },
                ],
            });
            console.log(subscription)

            // Save customer to organization metadata
            console.log('Adding stripe customer to organizations metadata')
            let metadata = event.organization.metadata
            metadata.stripe_customer = customer.id
            const data = { metadata: metadata }
            const params = { id: event.organization.id }
            const organization = await management.organizations.update(params, data)
            console.log(organization)

        }

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