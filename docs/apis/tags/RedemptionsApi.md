<a name="__pageTop"></a>
# versify.apis.tags.redemptions_api.RedemptionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_redemption_v2_redemptions_post**](#create_redemption_v2_redemptions_post) | **post** /v2/redemptions | Create redemption
[**create_redemption_v2_redemptions_post_0**](#create_redemption_v2_redemptions_post_0) | **post** /v2/redemptions | Create redemption
[**delete_redemption_v2_redemptions_redemption_id_delete**](#delete_redemption_v2_redemptions_redemption_id_delete) | **delete** /v2/redemptions/{redemption_id} | Delete redemption
[**delete_redemption_v2_redemptions_redemption_id_delete_0**](#delete_redemption_v2_redemptions_redemption_id_delete_0) | **delete** /v2/redemptions/{redemption_id} | Delete redemption
[**get_redemption_v2_redemptions_redemption_id_get**](#get_redemption_v2_redemptions_redemption_id_get) | **get** /v2/redemptions/{redemption_id} | Get redemption
[**get_redemption_v2_redemptions_redemption_id_get_0**](#get_redemption_v2_redemptions_redemption_id_get_0) | **get** /v2/redemptions/{redemption_id} | Get redemption
[**list_redemptions_v2_redemptions_get**](#list_redemptions_v2_redemptions_get) | **get** /v2/redemptions | List redemptions
[**list_redemptions_v2_redemptions_get_0**](#list_redemptions_v2_redemptions_get_0) | **get** /v2/redemptions | List redemptions
[**search_redemptions_v2_redemptions_search_post**](#search_redemptions_v2_redemptions_search_post) | **post** /v2/redemptions/search | Search redemptions
[**search_redemptions_v2_redemptions_search_post_0**](#search_redemptions_v2_redemptions_search_post_0) | **post** /v2/redemptions/search | Search redemptions
[**update_redemption_v2_redemptions_redemption_id_put**](#update_redemption_v2_redemptions_redemption_id_put) | **put** /v2/redemptions/{redemption_id} | Update redemption
[**update_redemption_v2_redemptions_redemption_id_put_0**](#update_redemption_v2_redemptions_redemption_id_put_0) | **put** /v2/redemptions/{redemption_id} | Update redemption

# **create_redemption_v2_redemptions_post**
<a name="create_redemption_v2_redemptions_post"></a>
> Redemption create_redemption_v2_redemptions_post(any_type)

Create redemption

Create a redemption

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
from versify.model.redemption import Redemption
from versify.model.http_validation_error import HTTPValidationError
from versify.model.redemption_create import RedemptionCreate
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Create redemption
        api_response = api_instance.create_redemption_v2_redemptions_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->create_redemption_v2_redemptions_post: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Create redemption
        api_response = api_instance.create_redemption_v2_redemptions_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->create_redemption_v2_redemptions_post: %s\n" % e)
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
[RedemptionCreate]({{complexTypePrefix}}RedemptionCreate.md) | [**RedemptionCreate**]({{complexTypePrefix}}RedemptionCreate.md) | [**RedemptionCreate**]({{complexTypePrefix}}RedemptionCreate.md) |  | 

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
201 | [ApiResponseFor201](#create_redemption_v2_redemptions_post.ApiResponseFor201) | The created redemption
422 | [ApiResponseFor422](#create_redemption_v2_redemptions_post.ApiResponseFor422) | Validation Error

#### create_redemption_v2_redemptions_post.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Redemption**](../../models/Redemption.md) |  | 


#### create_redemption_v2_redemptions_post.ApiResponseFor422
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

# **create_redemption_v2_redemptions_post_0**
<a name="create_redemption_v2_redemptions_post_0"></a>
> Redemption create_redemption_v2_redemptions_post_0(any_type)

Create redemption

Create a redemption

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
from versify.model.redemption import Redemption
from versify.model.http_validation_error import HTTPValidationError
from versify.model.redemption_create import RedemptionCreate
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Create redemption
        api_response = api_instance.create_redemption_v2_redemptions_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->create_redemption_v2_redemptions_post_0: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Create redemption
        api_response = api_instance.create_redemption_v2_redemptions_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->create_redemption_v2_redemptions_post_0: %s\n" % e)
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
[RedemptionCreate]({{complexTypePrefix}}RedemptionCreate.md) | [**RedemptionCreate**]({{complexTypePrefix}}RedemptionCreate.md) | [**RedemptionCreate**]({{complexTypePrefix}}RedemptionCreate.md) |  | 

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
201 | [ApiResponseFor201](#create_redemption_v2_redemptions_post_0.ApiResponseFor201) | The created redemption
422 | [ApiResponseFor422](#create_redemption_v2_redemptions_post_0.ApiResponseFor422) | Validation Error

#### create_redemption_v2_redemptions_post_0.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Redemption**](../../models/Redemption.md) |  | 


#### create_redemption_v2_redemptions_post_0.ApiResponseFor422
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

# **delete_redemption_v2_redemptions_redemption_id_delete**
<a name="delete_redemption_v2_redemptions_redemption_id_delete"></a>
> ApiDeleteResponse delete_redemption_v2_redemptions_redemption_id_delete(redemption_id)

Delete redemption

Delete an redemption

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Delete redemption
        api_response = api_instance.delete_redemption_v2_redemptions_redemption_id_delete(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->delete_redemption_v2_redemptions_redemption_id_delete: %s\n" % e)

    # example passing only optional values
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Delete redemption
        api_response = api_instance.delete_redemption_v2_redemptions_redemption_id_delete(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->delete_redemption_v2_redemptions_redemption_id_delete: %s\n" % e)
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
redemption_id | RedemptionIdSchema | | 

# RedemptionIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_redemption_v2_redemptions_redemption_id_delete.ApiResponseFor200) | The deleted redemption
422 | [ApiResponseFor422](#delete_redemption_v2_redemptions_redemption_id_delete.ApiResponseFor422) | Validation Error

#### delete_redemption_v2_redemptions_redemption_id_delete.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiDeleteResponse**](../../models/ApiDeleteResponse.md) |  | 


#### delete_redemption_v2_redemptions_redemption_id_delete.ApiResponseFor422
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

# **delete_redemption_v2_redemptions_redemption_id_delete_0**
<a name="delete_redemption_v2_redemptions_redemption_id_delete_0"></a>
> ApiDeleteResponse delete_redemption_v2_redemptions_redemption_id_delete_0(redemption_id)

Delete redemption

Delete an redemption

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Delete redemption
        api_response = api_instance.delete_redemption_v2_redemptions_redemption_id_delete_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->delete_redemption_v2_redemptions_redemption_id_delete_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Delete redemption
        api_response = api_instance.delete_redemption_v2_redemptions_redemption_id_delete_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->delete_redemption_v2_redemptions_redemption_id_delete_0: %s\n" % e)
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
redemption_id | RedemptionIdSchema | | 

# RedemptionIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_redemption_v2_redemptions_redemption_id_delete_0.ApiResponseFor200) | The deleted redemption
422 | [ApiResponseFor422](#delete_redemption_v2_redemptions_redemption_id_delete_0.ApiResponseFor422) | Validation Error

#### delete_redemption_v2_redemptions_redemption_id_delete_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiDeleteResponse**](../../models/ApiDeleteResponse.md) |  | 


#### delete_redemption_v2_redemptions_redemption_id_delete_0.ApiResponseFor422
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

# **get_redemption_v2_redemptions_redemption_id_get**
<a name="get_redemption_v2_redemptions_redemption_id_get"></a>
> Redemption get_redemption_v2_redemptions_redemption_id_get(redemption_id)

Get redemption

Get a redemption

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
from versify.model.redemption import Redemption
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Get redemption
        api_response = api_instance.get_redemption_v2_redemptions_redemption_id_get(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->get_redemption_v2_redemptions_redemption_id_get: %s\n" % e)

    # example passing only optional values
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Get redemption
        api_response = api_instance.get_redemption_v2_redemptions_redemption_id_get(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->get_redemption_v2_redemptions_redemption_id_get: %s\n" % e)
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
redemption_id | RedemptionIdSchema | | 

# RedemptionIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_redemption_v2_redemptions_redemption_id_get.ApiResponseFor200) | The redemption
422 | [ApiResponseFor422](#get_redemption_v2_redemptions_redemption_id_get.ApiResponseFor422) | Validation Error

#### get_redemption_v2_redemptions_redemption_id_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Redemption**](../../models/Redemption.md) |  | 


#### get_redemption_v2_redemptions_redemption_id_get.ApiResponseFor422
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

# **get_redemption_v2_redemptions_redemption_id_get_0**
<a name="get_redemption_v2_redemptions_redemption_id_get_0"></a>
> Redemption get_redemption_v2_redemptions_redemption_id_get_0(redemption_id)

Get redemption

Get a redemption

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
from versify.model.redemption import Redemption
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Get redemption
        api_response = api_instance.get_redemption_v2_redemptions_redemption_id_get_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->get_redemption_v2_redemptions_redemption_id_get_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Get redemption
        api_response = api_instance.get_redemption_v2_redemptions_redemption_id_get_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->get_redemption_v2_redemptions_redemption_id_get_0: %s\n" % e)
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
redemption_id | RedemptionIdSchema | | 

# RedemptionIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_redemption_v2_redemptions_redemption_id_get_0.ApiResponseFor200) | The redemption
422 | [ApiResponseFor422](#get_redemption_v2_redemptions_redemption_id_get_0.ApiResponseFor422) | Validation Error

#### get_redemption_v2_redemptions_redemption_id_get_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Redemption**](../../models/Redemption.md) |  | 


#### get_redemption_v2_redemptions_redemption_id_get_0.ApiResponseFor422
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

# **list_redemptions_v2_redemptions_get**
<a name="list_redemptions_v2_redemptions_get"></a>
> ApiListResponse list_redemptions_v2_redemptions_get()

List redemptions

List redemptions with optional filters and pagination parameters

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

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
        # List redemptions
        api_response = api_instance.list_redemptions_v2_redemptions_get(
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->list_redemptions_v2_redemptions_get: %s\n" % e)
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
200 | [ApiResponseFor200](#list_redemptions_v2_redemptions_get.ApiResponseFor200) | The list of redemptions
422 | [ApiResponseFor422](#list_redemptions_v2_redemptions_get.ApiResponseFor422) | Validation Error

#### list_redemptions_v2_redemptions_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiListResponse**](../../models/ApiListResponse.md) |  | 


#### list_redemptions_v2_redemptions_get.ApiResponseFor422
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

# **list_redemptions_v2_redemptions_get_0**
<a name="list_redemptions_v2_redemptions_get_0"></a>
> ApiListResponse list_redemptions_v2_redemptions_get_0()

List redemptions

List redemptions with optional filters and pagination parameters

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

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
        # List redemptions
        api_response = api_instance.list_redemptions_v2_redemptions_get_0(
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->list_redemptions_v2_redemptions_get_0: %s\n" % e)
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
200 | [ApiResponseFor200](#list_redemptions_v2_redemptions_get_0.ApiResponseFor200) | The list of redemptions
422 | [ApiResponseFor422](#list_redemptions_v2_redemptions_get_0.ApiResponseFor422) | Validation Error

#### list_redemptions_v2_redemptions_get_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiListResponse**](../../models/ApiListResponse.md) |  | 


#### list_redemptions_v2_redemptions_get_0.ApiResponseFor422
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

# **search_redemptions_v2_redemptions_search_post**
<a name="search_redemptions_v2_redemptions_search_post"></a>
> ApiSearchResponse search_redemptions_v2_redemptions_search_post(any_type)

Search redemptions

Search redemptions with query string

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Search redemptions
        api_response = api_instance.search_redemptions_v2_redemptions_search_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->search_redemptions_v2_redemptions_search_post: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Search redemptions
        api_response = api_instance.search_redemptions_v2_redemptions_search_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->search_redemptions_v2_redemptions_search_post: %s\n" % e)
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
200 | [ApiResponseFor200](#search_redemptions_v2_redemptions_search_post.ApiResponseFor200) | The list of redemptions
422 | [ApiResponseFor422](#search_redemptions_v2_redemptions_search_post.ApiResponseFor422) | Validation Error

#### search_redemptions_v2_redemptions_search_post.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiSearchResponse**](../../models/ApiSearchResponse.md) |  | 


#### search_redemptions_v2_redemptions_search_post.ApiResponseFor422
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

# **search_redemptions_v2_redemptions_search_post_0**
<a name="search_redemptions_v2_redemptions_search_post_0"></a>
> ApiSearchResponse search_redemptions_v2_redemptions_search_post_0(any_type)

Search redemptions

Search redemptions with query string

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Search redemptions
        api_response = api_instance.search_redemptions_v2_redemptions_search_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->search_redemptions_v2_redemptions_search_post_0: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Search redemptions
        api_response = api_instance.search_redemptions_v2_redemptions_search_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->search_redemptions_v2_redemptions_search_post_0: %s\n" % e)
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
200 | [ApiResponseFor200](#search_redemptions_v2_redemptions_search_post_0.ApiResponseFor200) | The list of redemptions
422 | [ApiResponseFor422](#search_redemptions_v2_redemptions_search_post_0.ApiResponseFor422) | Validation Error

#### search_redemptions_v2_redemptions_search_post_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiSearchResponse**](../../models/ApiSearchResponse.md) |  | 


#### search_redemptions_v2_redemptions_search_post_0.ApiResponseFor422
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

# **update_redemption_v2_redemptions_redemption_id_put**
<a name="update_redemption_v2_redemptions_redemption_id_put"></a>
> Redemption update_redemption_v2_redemptions_redemption_id_put(redemption_idany_type)

Update redemption

Update an redemption

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
from versify.model.redemption import Redemption
from versify.model.redemption_update import RedemptionUpdate
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
    }
    body = None
    try:
        # Update redemption
        api_response = api_instance.update_redemption_v2_redemptions_redemption_id_put(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->update_redemption_v2_redemptions_redemption_id_put: %s\n" % e)

    # example passing only optional values
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Update redemption
        api_response = api_instance.update_redemption_v2_redemptions_redemption_id_put(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->update_redemption_v2_redemptions_redemption_id_put: %s\n" % e)
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
[RedemptionUpdate]({{complexTypePrefix}}RedemptionUpdate.md) | [**RedemptionUpdate**]({{complexTypePrefix}}RedemptionUpdate.md) | [**RedemptionUpdate**]({{complexTypePrefix}}RedemptionUpdate.md) |  | 

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
redemption_id | RedemptionIdSchema | | 

# RedemptionIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_redemption_v2_redemptions_redemption_id_put.ApiResponseFor200) | The updated redemption
422 | [ApiResponseFor422](#update_redemption_v2_redemptions_redemption_id_put.ApiResponseFor422) | Validation Error

#### update_redemption_v2_redemptions_redemption_id_put.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Redemption**](../../models/Redemption.md) |  | 


#### update_redemption_v2_redemptions_redemption_id_put.ApiResponseFor422
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

# **update_redemption_v2_redemptions_redemption_id_put_0**
<a name="update_redemption_v2_redemptions_redemption_id_put_0"></a>
> Redemption update_redemption_v2_redemptions_redemption_id_put_0(redemption_idany_type)

Update redemption

Update an redemption

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import redemptions_api
from versify.model.redemption import Redemption
from versify.model.redemption_update import RedemptionUpdate
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
    api_instance = redemptions_api.RedemptionsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
    }
    body = None
    try:
        # Update redemption
        api_response = api_instance.update_redemption_v2_redemptions_redemption_id_put_0(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->update_redemption_v2_redemptions_redemption_id_put_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'redemption_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Update redemption
        api_response = api_instance.update_redemption_v2_redemptions_redemption_id_put_0(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling RedemptionsApi->update_redemption_v2_redemptions_redemption_id_put_0: %s\n" % e)
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
[RedemptionUpdate]({{complexTypePrefix}}RedemptionUpdate.md) | [**RedemptionUpdate**]({{complexTypePrefix}}RedemptionUpdate.md) | [**RedemptionUpdate**]({{complexTypePrefix}}RedemptionUpdate.md) |  | 

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
redemption_id | RedemptionIdSchema | | 

# RedemptionIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_redemption_v2_redemptions_redemption_id_put_0.ApiResponseFor200) | The updated redemption
422 | [ApiResponseFor422](#update_redemption_v2_redemptions_redemption_id_put_0.ApiResponseFor422) | Validation Error

#### update_redemption_v2_redemptions_redemption_id_put_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Redemption**](../../models/Redemption.md) |  | 


#### update_redemption_v2_redemptions_redemption_id_put_0.ApiResponseFor422
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

