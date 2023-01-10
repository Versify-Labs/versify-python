<a name="__pageTop"></a>
# versify.apis.tags.mints_api.MintsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_mint_v2_mints_post**](#create_mint_v2_mints_post) | **post** /v2/mints | Create mint
[**create_mint_v2_mints_post_0**](#create_mint_v2_mints_post_0) | **post** /v2/mints | Create mint
[**delete_mint_v2_mints_mint_id_delete**](#delete_mint_v2_mints_mint_id_delete) | **delete** /v2/mints/{mint_id} | Delete mint
[**delete_mint_v2_mints_mint_id_delete_0**](#delete_mint_v2_mints_mint_id_delete_0) | **delete** /v2/mints/{mint_id} | Delete mint
[**get_mint_v2_mints_mint_id_get**](#get_mint_v2_mints_mint_id_get) | **get** /v2/mints/{mint_id} | Get mint
[**get_mint_v2_mints_mint_id_get_0**](#get_mint_v2_mints_mint_id_get_0) | **get** /v2/mints/{mint_id} | Get mint
[**list_mints_v2_mints_get**](#list_mints_v2_mints_get) | **get** /v2/mints | List mints
[**list_mints_v2_mints_get_0**](#list_mints_v2_mints_get_0) | **get** /v2/mints | List mints
[**search_mints_v2_mints_search_post**](#search_mints_v2_mints_search_post) | **post** /v2/mints/search | Search mints
[**search_mints_v2_mints_search_post_0**](#search_mints_v2_mints_search_post_0) | **post** /v2/mints/search | Search mints
[**update_mint_v2_mints_mint_id_put**](#update_mint_v2_mints_mint_id_put) | **put** /v2/mints/{mint_id} | Update mint
[**update_mint_v2_mints_mint_id_put_0**](#update_mint_v2_mints_mint_id_put_0) | **put** /v2/mints/{mint_id} | Update mint

# **create_mint_v2_mints_post**
<a name="create_mint_v2_mints_post"></a>
> Mint create_mint_v2_mints_post(any_type)

Create mint

Create a mint

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.mint import Mint
from versify.model.mint_create import MintCreate
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Create mint
        api_response = api_instance.create_mint_v2_mints_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->create_mint_v2_mints_post: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Create mint
        api_response = api_instance.create_mint_v2_mints_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->create_mint_v2_mints_post: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
header_params | RequestHeaderParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

Asset to create

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Asset to create | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[MintCreate]({{complexTypePrefix}}MintCreate.md) | [**MintCreate**]({{complexTypePrefix}}MintCreate.md) | [**MintCreate**]({{complexTypePrefix}}MintCreate.md) |  | 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_mint_v2_mints_post.ApiResponseFor201) | The created mint
422 | [ApiResponseFor422](#create_mint_v2_mints_post.ApiResponseFor422) | Validation Error

#### create_mint_v2_mints_post.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Mint**](../../models/Mint.md) |  | 


#### create_mint_v2_mints_post.ApiResponseFor422
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

# **create_mint_v2_mints_post_0**
<a name="create_mint_v2_mints_post_0"></a>
> Mint create_mint_v2_mints_post_0(any_type)

Create mint

Create a mint

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.mint import Mint
from versify.model.mint_create import MintCreate
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Create mint
        api_response = api_instance.create_mint_v2_mints_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->create_mint_v2_mints_post_0: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Create mint
        api_response = api_instance.create_mint_v2_mints_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->create_mint_v2_mints_post_0: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
header_params | RequestHeaderParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

Asset to create

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Asset to create | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[MintCreate]({{complexTypePrefix}}MintCreate.md) | [**MintCreate**]({{complexTypePrefix}}MintCreate.md) | [**MintCreate**]({{complexTypePrefix}}MintCreate.md) |  | 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_mint_v2_mints_post_0.ApiResponseFor201) | The created mint
422 | [ApiResponseFor422](#create_mint_v2_mints_post_0.ApiResponseFor422) | Validation Error

#### create_mint_v2_mints_post_0.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Mint**](../../models/Mint.md) |  | 


#### create_mint_v2_mints_post_0.ApiResponseFor422
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

# **delete_mint_v2_mints_mint_id_delete**
<a name="delete_mint_v2_mints_mint_id_delete"></a>
> ApiDeleteResponse delete_mint_v2_mints_mint_id_delete(mint_id)

Delete mint

Delete an mint

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Delete mint
        api_response = api_instance.delete_mint_v2_mints_mint_id_delete(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->delete_mint_v2_mints_mint_id_delete: %s\n" % e)

    # example passing only optional values
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Delete mint
        api_response = api_instance.delete_mint_v2_mints_mint_id_delete(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->delete_mint_v2_mints_mint_id_delete: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
mint_id | MintIdSchema | | 

# MintIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_mint_v2_mints_mint_id_delete.ApiResponseFor200) | The deleted mint
422 | [ApiResponseFor422](#delete_mint_v2_mints_mint_id_delete.ApiResponseFor422) | Validation Error

#### delete_mint_v2_mints_mint_id_delete.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiDeleteResponse**](../../models/ApiDeleteResponse.md) |  | 


#### delete_mint_v2_mints_mint_id_delete.ApiResponseFor422
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

# **delete_mint_v2_mints_mint_id_delete_0**
<a name="delete_mint_v2_mints_mint_id_delete_0"></a>
> ApiDeleteResponse delete_mint_v2_mints_mint_id_delete_0(mint_id)

Delete mint

Delete an mint

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Delete mint
        api_response = api_instance.delete_mint_v2_mints_mint_id_delete_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->delete_mint_v2_mints_mint_id_delete_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Delete mint
        api_response = api_instance.delete_mint_v2_mints_mint_id_delete_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->delete_mint_v2_mints_mint_id_delete_0: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
mint_id | MintIdSchema | | 

# MintIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_mint_v2_mints_mint_id_delete_0.ApiResponseFor200) | The deleted mint
422 | [ApiResponseFor422](#delete_mint_v2_mints_mint_id_delete_0.ApiResponseFor422) | Validation Error

#### delete_mint_v2_mints_mint_id_delete_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiDeleteResponse**](../../models/ApiDeleteResponse.md) |  | 


#### delete_mint_v2_mints_mint_id_delete_0.ApiResponseFor422
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

# **get_mint_v2_mints_mint_id_get**
<a name="get_mint_v2_mints_mint_id_get"></a>
> Mint get_mint_v2_mints_mint_id_get(mint_id)

Get mint

Get a mint

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.mint import Mint
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Get mint
        api_response = api_instance.get_mint_v2_mints_mint_id_get(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->get_mint_v2_mints_mint_id_get: %s\n" % e)

    # example passing only optional values
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Get mint
        api_response = api_instance.get_mint_v2_mints_mint_id_get(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->get_mint_v2_mints_mint_id_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
mint_id | MintIdSchema | | 

# MintIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_mint_v2_mints_mint_id_get.ApiResponseFor200) | The mint
422 | [ApiResponseFor422](#get_mint_v2_mints_mint_id_get.ApiResponseFor422) | Validation Error

#### get_mint_v2_mints_mint_id_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Mint**](../../models/Mint.md) |  | 


#### get_mint_v2_mints_mint_id_get.ApiResponseFor422
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

# **get_mint_v2_mints_mint_id_get_0**
<a name="get_mint_v2_mints_mint_id_get_0"></a>
> Mint get_mint_v2_mints_mint_id_get_0(mint_id)

Get mint

Get a mint

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.mint import Mint
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Get mint
        api_response = api_instance.get_mint_v2_mints_mint_id_get_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->get_mint_v2_mints_mint_id_get_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Get mint
        api_response = api_instance.get_mint_v2_mints_mint_id_get_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->get_mint_v2_mints_mint_id_get_0: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
mint_id | MintIdSchema | | 

# MintIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_mint_v2_mints_mint_id_get_0.ApiResponseFor200) | The mint
422 | [ApiResponseFor422](#get_mint_v2_mints_mint_id_get_0.ApiResponseFor422) | Validation Error

#### get_mint_v2_mints_mint_id_get_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Mint**](../../models/Mint.md) |  | 


#### get_mint_v2_mints_mint_id_get_0.ApiResponseFor422
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

# **list_mints_v2_mints_get**
<a name="list_mints_v2_mints_get"></a>
> ApiListResponse list_mints_v2_mints_get()

List mints

List mints with optional filters and pagination parameters

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.api_list_response import ApiListResponse
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only optional values
    query_params = {
        'page_num': 1,
        'page_size': 10,
        'collection': "col_12121231231231321",
        'status': "active",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # List mints
        api_response = api_instance.list_mints_v2_mints_get(
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->list_mints_v2_mints_get: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
page_num | PageNumSchema | | optional
page_size | PageSizeSchema | | optional
collection | CollectionSchema | | optional
status | StatusSchema | | optional


# PageNumSchema

Page number

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  | Page number | if omitted the server will use the default value of 1

# PageSizeSchema

Page size

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  | Page size | if omitted the server will use the default value of 10

# CollectionSchema

Collection ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Collection ID | 

# StatusSchema

Collection status

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Collection status | 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#list_mints_v2_mints_get.ApiResponseFor200) | The list of mints
422 | [ApiResponseFor422](#list_mints_v2_mints_get.ApiResponseFor422) | Validation Error

#### list_mints_v2_mints_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiListResponse**](../../models/ApiListResponse.md) |  | 


#### list_mints_v2_mints_get.ApiResponseFor422
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

# **list_mints_v2_mints_get_0**
<a name="list_mints_v2_mints_get_0"></a>
> ApiListResponse list_mints_v2_mints_get_0()

List mints

List mints with optional filters and pagination parameters

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.api_list_response import ApiListResponse
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only optional values
    query_params = {
        'page_num': 1,
        'page_size': 10,
        'collection': "col_12121231231231321",
        'status': "active",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # List mints
        api_response = api_instance.list_mints_v2_mints_get_0(
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->list_mints_v2_mints_get_0: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
page_num | PageNumSchema | | optional
page_size | PageSizeSchema | | optional
collection | CollectionSchema | | optional
status | StatusSchema | | optional


# PageNumSchema

Page number

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  | Page number | if omitted the server will use the default value of 1

# PageSizeSchema

Page size

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  | Page size | if omitted the server will use the default value of 10

# CollectionSchema

Collection ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Collection ID | 

# StatusSchema

Collection status

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Collection status | 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#list_mints_v2_mints_get_0.ApiResponseFor200) | The list of mints
422 | [ApiResponseFor422](#list_mints_v2_mints_get_0.ApiResponseFor422) | Validation Error

#### list_mints_v2_mints_get_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiListResponse**](../../models/ApiListResponse.md) |  | 


#### list_mints_v2_mints_get_0.ApiResponseFor422
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

# **search_mints_v2_mints_search_post**
<a name="search_mints_v2_mints_search_post"></a>
> ApiSearchResponse search_mints_v2_mints_search_post(any_type)

Search mints

Search mints with query string

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.api_search_response import ApiSearchResponse
from versify.model.search_query import SearchQuery
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Search mints
        api_response = api_instance.search_mints_v2_mints_search_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->search_mints_v2_mints_search_post: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Search mints
        api_response = api_instance.search_mints_v2_mints_search_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->search_mints_v2_mints_search_post: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
header_params | RequestHeaderParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

Search contacts

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Search contacts | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[SearchQuery]({{complexTypePrefix}}SearchQuery.md) | [**SearchQuery**]({{complexTypePrefix}}SearchQuery.md) | [**SearchQuery**]({{complexTypePrefix}}SearchQuery.md) |  | 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#search_mints_v2_mints_search_post.ApiResponseFor200) | The list of mints
422 | [ApiResponseFor422](#search_mints_v2_mints_search_post.ApiResponseFor422) | Validation Error

#### search_mints_v2_mints_search_post.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiSearchResponse**](../../models/ApiSearchResponse.md) |  | 


#### search_mints_v2_mints_search_post.ApiResponseFor422
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

# **search_mints_v2_mints_search_post_0**
<a name="search_mints_v2_mints_search_post_0"></a>
> ApiSearchResponse search_mints_v2_mints_search_post_0(any_type)

Search mints

Search mints with query string

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.api_search_response import ApiSearchResponse
from versify.model.search_query import SearchQuery
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Search mints
        api_response = api_instance.search_mints_v2_mints_search_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->search_mints_v2_mints_search_post_0: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Search mints
        api_response = api_instance.search_mints_v2_mints_search_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->search_mints_v2_mints_search_post_0: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
header_params | RequestHeaderParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

Search contacts

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Search contacts | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[SearchQuery]({{complexTypePrefix}}SearchQuery.md) | [**SearchQuery**]({{complexTypePrefix}}SearchQuery.md) | [**SearchQuery**]({{complexTypePrefix}}SearchQuery.md) |  | 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#search_mints_v2_mints_search_post_0.ApiResponseFor200) | The list of mints
422 | [ApiResponseFor422](#search_mints_v2_mints_search_post_0.ApiResponseFor422) | Validation Error

#### search_mints_v2_mints_search_post_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiSearchResponse**](../../models/ApiSearchResponse.md) |  | 


#### search_mints_v2_mints_search_post_0.ApiResponseFor422
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

# **update_mint_v2_mints_mint_id_put**
<a name="update_mint_v2_mints_mint_id_put"></a>
> Mint update_mint_v2_mints_mint_id_put(mint_idany_type)

Update mint

Update an mint

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.mint_update import MintUpdate
from versify.model.mint import Mint
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
    }
    body = None
    try:
        # Update mint
        api_response = api_instance.update_mint_v2_mints_mint_id_put(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->update_mint_v2_mints_mint_id_put: %s\n" % e)

    # example passing only optional values
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Update mint
        api_response = api_instance.update_mint_v2_mints_mint_id_put(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->update_mint_v2_mints_mint_id_put: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

Contact to update

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Contact to update | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[MintUpdate]({{complexTypePrefix}}MintUpdate.md) | [**MintUpdate**]({{complexTypePrefix}}MintUpdate.md) | [**MintUpdate**]({{complexTypePrefix}}MintUpdate.md) |  | 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
mint_id | MintIdSchema | | 

# MintIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_mint_v2_mints_mint_id_put.ApiResponseFor200) | The updated mint
422 | [ApiResponseFor422](#update_mint_v2_mints_mint_id_put.ApiResponseFor422) | Validation Error

#### update_mint_v2_mints_mint_id_put.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Mint**](../../models/Mint.md) |  | 


#### update_mint_v2_mints_mint_id_put.ApiResponseFor422
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

# **update_mint_v2_mints_mint_id_put_0**
<a name="update_mint_v2_mints_mint_id_put_0"></a>
> Mint update_mint_v2_mints_mint_id_put_0(mint_idany_type)

Update mint

Update an mint

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import mints_api
from versify.model.mint_update import MintUpdate
from versify.model.mint import Mint
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
    api_instance = mints_api.MintsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
    }
    body = None
    try:
        # Update mint
        api_response = api_instance.update_mint_v2_mints_mint_id_put_0(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->update_mint_v2_mints_mint_id_put_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'mint_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Update mint
        api_response = api_instance.update_mint_v2_mints_mint_id_put_0(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling MintsApi->update_mint_v2_mints_mint_id_put_0: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson

Contact to update

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Contact to update | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[MintUpdate]({{complexTypePrefix}}MintUpdate.md) | [**MintUpdate**]({{complexTypePrefix}}MintUpdate.md) | [**MintUpdate**]({{complexTypePrefix}}MintUpdate.md) |  | 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
Versify-Account | VersifyAccountSchema | | optional

# VersifyAccountSchema

Versify Account ID

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Versify Account ID | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
mint_id | MintIdSchema | | 

# MintIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_mint_v2_mints_mint_id_put_0.ApiResponseFor200) | The updated mint
422 | [ApiResponseFor422](#update_mint_v2_mints_mint_id_put_0.ApiResponseFor422) | Validation Error

#### update_mint_v2_mints_mint_id_put_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Mint**](../../models/Mint.md) |  | 


#### update_mint_v2_mints_mint_id_put_0.ApiResponseFor422
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

