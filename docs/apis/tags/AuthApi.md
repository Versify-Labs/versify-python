<a name="__pageTop"></a>
# versify.apis.tags.auth_api.AuthApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**access_token_v2_oauth_access_token_post**](#access_token_v2_oauth_access_token_post) | **post** /v2/oauth/access_token | Access Token
[**access_token_v2_oauth_access_token_post_0**](#access_token_v2_oauth_access_token_post_0) | **post** /v2/oauth/access_token | Access Token
[**authorize_v2_oauth_authorize_get**](#authorize_v2_oauth_authorize_get) | **get** /v2/oauth/authorize | Authorize
[**authorize_v2_oauth_authorize_get_0**](#authorize_v2_oauth_authorize_get_0) | **get** /v2/oauth/authorize | Authorize

# **access_token_v2_oauth_access_token_post**
<a name="access_token_v2_oauth_access_token_post"></a>
> bool, date, datetime, dict, float, int, list, str, none_type access_token_v2_oauth_access_token_post(body_access_token_v2_oauth_access_token_post)

Access Token

### Example

```python
import versify
from versify.apis.tags import auth_api
from versify.model.body_access_token_v2_oauth_access_token_post import BodyAccessTokenV2OauthAccessTokenPost
from versify.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = auth_api.AuthApi(api_client)

    # example passing only required values which don't have defaults set
    body = BodyAccessTokenV2OauthAccessTokenPost(
        code="code_example",
        custom_claims=dict(),
        method_id="method_id_example",
    )
    try:
        # Access Token
        api_response = api_instance.access_token_v2_oauth_access_token_post(
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AuthApi->access_token_v2_oauth_access_token_post: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**BodyAccessTokenV2OauthAccessTokenPost**](../../models/BodyAccessTokenV2OauthAccessTokenPost.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#access_token_v2_oauth_access_token_post.ApiResponseFor200) | Successful Response
422 | [ApiResponseFor422](#access_token_v2_oauth_access_token_post.ApiResponseFor422) | Validation Error

#### access_token_v2_oauth_access_token_post.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

#### access_token_v2_oauth_access_token_post.ApiResponseFor422
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor422ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor422ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**HTTPValidationError**](../../models/HTTPValidationError.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **access_token_v2_oauth_access_token_post_0**
<a name="access_token_v2_oauth_access_token_post_0"></a>
> bool, date, datetime, dict, float, int, list, str, none_type access_token_v2_oauth_access_token_post_0(body_access_token_v2_oauth_access_token_post)

Access Token

### Example

```python
import versify
from versify.apis.tags import auth_api
from versify.model.body_access_token_v2_oauth_access_token_post import BodyAccessTokenV2OauthAccessTokenPost
from versify.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = auth_api.AuthApi(api_client)

    # example passing only required values which don't have defaults set
    body = BodyAccessTokenV2OauthAccessTokenPost(
        code="code_example",
        custom_claims=dict(),
        method_id="method_id_example",
    )
    try:
        # Access Token
        api_response = api_instance.access_token_v2_oauth_access_token_post_0(
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AuthApi->access_token_v2_oauth_access_token_post_0: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**BodyAccessTokenV2OauthAccessTokenPost**](../../models/BodyAccessTokenV2OauthAccessTokenPost.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#access_token_v2_oauth_access_token_post_0.ApiResponseFor200) | Successful Response
422 | [ApiResponseFor422](#access_token_v2_oauth_access_token_post_0.ApiResponseFor422) | Validation Error

#### access_token_v2_oauth_access_token_post_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

#### access_token_v2_oauth_access_token_post_0.ApiResponseFor422
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor422ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor422ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**HTTPValidationError**](../../models/HTTPValidationError.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **authorize_v2_oauth_authorize_get**
<a name="authorize_v2_oauth_authorize_get"></a>
> bool, date, datetime, dict, float, int, list, str, none_type authorize_v2_oauth_authorize_get(response_typeclient_idredirect_uri)

Authorize

### Example

```python
import versify
from versify.apis.tags import auth_api
from versify.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = auth_api.AuthApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'response_type': "code",
        'client_id': "",
        'redirect_uri': "https://oauth.pstmn.io/v1/browser-callback",
    }
    try:
        # Authorize
        api_response = api_instance.authorize_v2_oauth_authorize_get(
            query_params=query_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AuthApi->authorize_v2_oauth_authorize_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response_type | ResponseTypeSchema | | 
client_id | ClientIdSchema | | 
redirect_uri | RedirectUriSchema | | 


# ResponseTypeSchema

The type of response to return.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | The type of response to return. | 

# ClientIdSchema

The client ID to use for authentication.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | The client ID to use for authentication. | 

# RedirectUriSchema

The redirect URI to use for authentication.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | The redirect URI to use for authentication. | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#authorize_v2_oauth_authorize_get.ApiResponseFor200) | Successful Response
422 | [ApiResponseFor422](#authorize_v2_oauth_authorize_get.ApiResponseFor422) | Validation Error

#### authorize_v2_oauth_authorize_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

#### authorize_v2_oauth_authorize_get.ApiResponseFor422
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor422ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor422ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**HTTPValidationError**](../../models/HTTPValidationError.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **authorize_v2_oauth_authorize_get_0**
<a name="authorize_v2_oauth_authorize_get_0"></a>
> bool, date, datetime, dict, float, int, list, str, none_type authorize_v2_oauth_authorize_get_0(response_typeclient_idredirect_uri)

Authorize

### Example

```python
import versify
from versify.apis.tags import auth_api
from versify.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = auth_api.AuthApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
        'response_type': "code",
        'client_id': "",
        'redirect_uri': "https://oauth.pstmn.io/v1/browser-callback",
    }
    try:
        # Authorize
        api_response = api_instance.authorize_v2_oauth_authorize_get_0(
            query_params=query_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AuthApi->authorize_v2_oauth_authorize_get_0: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response_type | ResponseTypeSchema | | 
client_id | ClientIdSchema | | 
redirect_uri | RedirectUriSchema | | 


# ResponseTypeSchema

The type of response to return.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | The type of response to return. | 

# ClientIdSchema

The client ID to use for authentication.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | The client ID to use for authentication. | 

# RedirectUriSchema

The redirect URI to use for authentication.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | The redirect URI to use for authentication. | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#authorize_v2_oauth_authorize_get_0.ApiResponseFor200) | Successful Response
422 | [ApiResponseFor422](#authorize_v2_oauth_authorize_get_0.ApiResponseFor422) | Validation Error

#### authorize_v2_oauth_authorize_get_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

#### authorize_v2_oauth_authorize_get_0.ApiResponseFor422
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor422ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor422ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**HTTPValidationError**](../../models/HTTPValidationError.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

