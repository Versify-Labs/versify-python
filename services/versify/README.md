# Versify API


## Structure

Models
Services
Controllers
Jobs
Subscribers


## OAuth 2.0

### OAuth 2.0 Roles

- Resource Owner: Entity that can grant access to a protected resource. In our case, our customer accounts.
- Resource Server: Server hosting the protected resources. This is the API you want to access. In our case, the Versify API.
- Client: Application requesting access to a protected resource on behalf of the Resource Owner. In our case, this is either the Versify dashboard, 3P Apps (Zapier, Shopify, etc)
- Authorization Server: Server that authenticates the Resource Owner and issues access tokens after getting proper authorization. In our case, Auth0.

### Grant Types

- Versify Dashboard: Implicit Flow
- Versify Services: Client Credentials Flow
- 3p Services: Authorization Code Flow

### Endpoints

#### Authorization Endpoint

- Endpoint: `/authorize`
- Description: Used to interact with the resource owner and get the authorization to access the protected resource.

```
# Versify Dashboard Example (Implicit Flow)
{
    response_type: 'test',
    response_mode: '',
    client_id: '',
    redirect_uri: '',
    scope: '',
    state: ''
}

# Versify Dashboard Example (Authorization Code Flow)
{
    response_type: 'test',
    response_mode: '',
    client_id: '',
    redirect_uri: '',
    scope: '',
    state: ''
}
```

#### Token Endpoint

- Endpoint: `/oauth/token`
- Description: Used by the application in order to get an access token or refresh token.
- Example:

### Flows

#### Implicit Flow

```sh
# Request access token (/authorize)
{
    response_type: 'token',
    response_mode: '',
    client_id: '',
    redirect_uri: '',
    scope: '',
    state: ''
}

# Receive JWT
```

#### Authorization Code Flow

```sh

# The user clicks Login

# Auth0's SDK redirects the user to the Auth0 Authorization Server (/authorize endpoint).
curl GET https://$DOMAIN/authorize?
  audience=$API_IDENTIFIER&
  client_id=$CLIENT_ID&
  response_type=$RESPONSE_TYPE&
  redirect_uri=$REDIRECT_URI&
  scope=$SCOPE&
  state=STATE

# Your Auth0 Authorization Server redirects the user to the login and authorization prompt.

# The user authenticates using one of the configured login options and may see a consent page listing the permissions Auth0 will give to the regular web application.

# Your Auth0 Authorization Server redirects the user back to the application with an authorization code, which is good for one use.

# Auth0's SDK sends this code to the Auth0 Authorization Server (/oauth/token endpoint) along with the application's Client ID and Client Secret.
curl POST https://$DOMAIN/oauth/token?
  audience=$API_IDENTIFIER&
  client_id=$CLIENT_ID&
  client_secret=$CLIENT_SECRET&
  response_type=$RESPONSE_TYPE&
  redirect_uri=$REDIRECT_URI&
  scope=$SCOPE&
  state=STATE

# Your Auth0 Authorization Server verifies the code, Client ID, and Client Secret.

# Your Auth0 Authorization Server responds with an ID Token and Access Token (and optionally, a Refresh Token).

# Your application can use the Access Token to call an API to access information about the user.

# The API responds with requested data.

```
