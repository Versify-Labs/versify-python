<a name="__pageTop"></a>
# versify.apis.tags.accounts_api.AccountsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_account_v2_accounts_post**](#create_account_v2_accounts_post) | **post** /v2/accounts | Create an account
[**delete_account_v2_accounts_account_id_delete**](#delete_account_v2_accounts_account_id_delete) | **delete** /v2/accounts/{account_id} | Delete an account
[**get_account_metrics_v2_accounts_account_id_metrics_get**](#get_account_metrics_v2_accounts_account_id_metrics_get) | **get** /v2/accounts/{account_id}/metrics | Get account metrics
[**get_account_v2_accounts_account_id_get**](#get_account_v2_accounts_account_id_get) | **get** /v2/accounts/{account_id} | Get an account
[**list_accounts_v2_accounts_get**](#list_accounts_v2_accounts_get) | **get** /v2/accounts | List accounts
[**update_account_v2_accounts_account_id_put**](#update_account_v2_accounts_account_id_put) | **put** /v2/accounts/{account_id} | Update an account

# **create_account_v2_accounts_post**
<a name="create_account_v2_accounts_post"></a>
> Account create_account_v2_accounts_post(any_type)

Create an account

Create an account

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import accounts_api
from versify.model.account import Account
from versify.model.http_validation_error import HTTPValidationError
from versify.model.account_create import AccountCreate
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = versify.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accounts_api.AccountsApi(api_client)

    # example passing only required values which don't have defaults set
    body = None
    try:
        # Create an account
        api_response = api_instance.create_account_v2_accounts_post(
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AccountsApi->create_account_v2_accounts_post: %s\n" % e)
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

Account to create

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Account to create | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AccountCreate]({{complexTypePrefix}}AccountCreate.md) | [**AccountCreate**]({{complexTypePrefix}}AccountCreate.md) | [**AccountCreate**]({{complexTypePrefix}}AccountCreate.md) |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_account_v2_accounts_post.ApiResponseFor201) | The created account
422 | [ApiResponseFor422](#create_account_v2_accounts_post.ApiResponseFor422) | Validation Error

#### create_account_v2_accounts_post.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Account**](../../models/Account.md) |  | 


#### create_account_v2_accounts_post.ApiResponseFor422
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

[HTTPBearer](../../../README.md#HTTPBearer)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_account_v2_accounts_account_id_delete**
<a name="delete_account_v2_accounts_account_id_delete"></a>
> ApiDeleteResponse delete_account_v2_accounts_account_id_delete(account_id)

Delete an account

Delete an account by ID

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import accounts_api
from versify.model.api_delete_response import ApiDeleteResponse
from versify.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = versify.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accounts_api.AccountsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'account_id': "act_2323213123123123",
    }
    try:
        # Delete an account
        api_response = api_instance.delete_account_v2_accounts_account_id_delete(
            path_params=path_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AccountsApi->delete_account_v2_accounts_account_id_delete: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
account_id | AccountIdSchema | | 

# AccountIdSchema

Unique identifier of the account

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the account | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_account_v2_accounts_account_id_delete.ApiResponseFor200) | The deleted account
422 | [ApiResponseFor422](#delete_account_v2_accounts_account_id_delete.ApiResponseFor422) | Validation Error

#### delete_account_v2_accounts_account_id_delete.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiDeleteResponse**](../../models/ApiDeleteResponse.md) |  | 


#### delete_account_v2_accounts_account_id_delete.ApiResponseFor422
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

[HTTPBearer](../../../README.md#HTTPBearer)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_account_metrics_v2_accounts_account_id_metrics_get**
<a name="get_account_metrics_v2_accounts_account_id_metrics_get"></a>
> AccountMetrics get_account_metrics_v2_accounts_account_id_metrics_get(account_id)

Get account metrics

Get account metrics by ID

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import accounts_api
from versify.model.account_metrics import AccountMetrics
from versify.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = versify.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accounts_api.AccountsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'account_id': "act_2323213123123123",
    }
    query_params = {
    }
    try:
        # Get account metrics
        api_response = api_instance.get_account_metrics_v2_accounts_account_id_metrics_get(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AccountsApi->get_account_metrics_v2_accounts_account_id_metrics_get: %s\n" % e)

    # example passing only optional values
    path_params = {
        'account_id': "act_2323213123123123",
    }
    query_params = {
        'object_types': [
        "contact"
    ],
    }
    try:
        # Get account metrics
        api_response = api_instance.get_account_metrics_v2_accounts_account_id_metrics_get(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AccountsApi->get_account_metrics_v2_accounts_account_id_metrics_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
object_types | ObjectTypesSchema | | optional


# ObjectTypesSchema

Object types

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Object types | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
account_id | AccountIdSchema | | 

# AccountIdSchema

Unique identifier of the account

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the account | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_account_metrics_v2_accounts_account_id_metrics_get.ApiResponseFor200) | The account
422 | [ApiResponseFor422](#get_account_metrics_v2_accounts_account_id_metrics_get.ApiResponseFor422) | Validation Error

#### get_account_metrics_v2_accounts_account_id_metrics_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**AccountMetrics**](../../models/AccountMetrics.md) |  | 


#### get_account_metrics_v2_accounts_account_id_metrics_get.ApiResponseFor422
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

[HTTPBearer](../../../README.md#HTTPBearer)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_account_v2_accounts_account_id_get**
<a name="get_account_v2_accounts_account_id_get"></a>
> Account get_account_v2_accounts_account_id_get(account_id)

Get an account

Get an account by ID

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import accounts_api
from versify.model.account import Account
from versify.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = versify.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accounts_api.AccountsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'account_id': "act_2323213123123123",
    }
    try:
        # Get an account
        api_response = api_instance.get_account_v2_accounts_account_id_get(
            path_params=path_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AccountsApi->get_account_v2_accounts_account_id_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
account_id | AccountIdSchema | | 

# AccountIdSchema

Unique identifier of the account

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the account | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_account_v2_accounts_account_id_get.ApiResponseFor200) | The account
422 | [ApiResponseFor422](#get_account_v2_accounts_account_id_get.ApiResponseFor422) | Validation Error

#### get_account_v2_accounts_account_id_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Account**](../../models/Account.md) |  | 


#### get_account_v2_accounts_account_id_get.ApiResponseFor422
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

[HTTPBearer](../../../README.md#HTTPBearer)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **list_accounts_v2_accounts_get**
<a name="list_accounts_v2_accounts_get"></a>
> ApiListResponse list_accounts_v2_accounts_get()

List accounts

List accounts with optional filters and pagination parameters

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import accounts_api
from versify.model.api_list_response import ApiListResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = versify.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accounts_api.AccountsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # List accounts
        api_response = api_instance.list_accounts_v2_accounts_get()
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AccountsApi->list_accounts_v2_accounts_get: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#list_accounts_v2_accounts_get.ApiResponseFor200) | The list of accounts

#### list_accounts_v2_accounts_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiListResponse**](../../models/ApiListResponse.md) |  | 


### Authorization

[HTTPBearer](../../../README.md#HTTPBearer)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_account_v2_accounts_account_id_put**
<a name="update_account_v2_accounts_account_id_put"></a>
> Account update_account_v2_accounts_account_id_put(account_idany_type)

Update an account

Update an account by ID

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import accounts_api
from versify.model.account import Account
from versify.model.account_update import AccountUpdate
from versify.model.http_validation_error import HTTPValidationError
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = versify.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: HTTPBearer
configuration = versify.Configuration(
    access_token = 'YOUR_BEARER_TOKEN'
)
# Enter a context with an instance of the API client
with versify.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = accounts_api.AccountsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'account_id': "act_2323213123123123",
    }
    body = None
    try:
        # Update an account
        api_response = api_instance.update_account_v2_accounts_account_id_put(
            path_params=path_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling AccountsApi->update_account_v2_accounts_account_id_put: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

Account to update

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Account to update | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AccountUpdate]({{complexTypePrefix}}AccountUpdate.md) | [**AccountUpdate**]({{complexTypePrefix}}AccountUpdate.md) | [**AccountUpdate**]({{complexTypePrefix}}AccountUpdate.md) |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
account_id | AccountIdSchema | | 

# AccountIdSchema

Unique identifier of the account

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the account | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_account_v2_accounts_account_id_put.ApiResponseFor200) | The updated account
422 | [ApiResponseFor422](#update_account_v2_accounts_account_id_put.ApiResponseFor422) | Validation Error

#### update_account_v2_accounts_account_id_put.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Account**](../../models/Account.md) |  | 


#### update_account_v2_accounts_account_id_put.ApiResponseFor422
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

[HTTPBearer](../../../README.md#HTTPBearer)

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

