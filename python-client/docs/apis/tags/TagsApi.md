<a name="__pageTop"></a>
# versify.apis.tags.tags_api.TagsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_tag_v2_tags_post**](#create_tag_v2_tags_post) | **post** /v2/tags | Create tag
[**create_tag_v2_tags_post_0**](#create_tag_v2_tags_post_0) | **post** /v2/tags | Create tag
[**delete_tag_v2_tags_tag_id_delete**](#delete_tag_v2_tags_tag_id_delete) | **delete** /v2/tags/{tag_id} | Delete tag
[**delete_tag_v2_tags_tag_id_delete_0**](#delete_tag_v2_tags_tag_id_delete_0) | **delete** /v2/tags/{tag_id} | Delete tag
[**get_tag_v2_tags_tag_id_get**](#get_tag_v2_tags_tag_id_get) | **get** /v2/tags/{tag_id} | Get tag
[**get_tag_v2_tags_tag_id_get_0**](#get_tag_v2_tags_tag_id_get_0) | **get** /v2/tags/{tag_id} | Get tag
[**list_tags_v2_tags_get**](#list_tags_v2_tags_get) | **get** /v2/tags | List tags
[**list_tags_v2_tags_get_0**](#list_tags_v2_tags_get_0) | **get** /v2/tags | List tags
[**search_tags_v2_tags_search_post**](#search_tags_v2_tags_search_post) | **post** /v2/tags/search | Search tags
[**search_tags_v2_tags_search_post_0**](#search_tags_v2_tags_search_post_0) | **post** /v2/tags/search | Search tags
[**update_tag_v2_tags_tag_id_put**](#update_tag_v2_tags_tag_id_put) | **put** /v2/tags/{tag_id} | Update tag
[**update_tag_v2_tags_tag_id_put_0**](#update_tag_v2_tags_tag_id_put_0) | **put** /v2/tags/{tag_id} | Update tag

# **create_tag_v2_tags_post**
<a name="create_tag_v2_tags_post"></a>
> Tag create_tag_v2_tags_post(any_type)

Create tag

Create a tag

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
from versify.model.tag import Tag
from versify.model.http_validation_error import HTTPValidationError
from versify.model.tag_create import TagCreate
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Create tag
        api_response = api_instance.create_tag_v2_tags_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->create_tag_v2_tags_post: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Create tag
        api_response = api_instance.create_tag_v2_tags_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->create_tag_v2_tags_post: %s\n" % e)
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
[TagCreate]({{complexTypePrefix}}TagCreate.md) | [**TagCreate**]({{complexTypePrefix}}TagCreate.md) | [**TagCreate**]({{complexTypePrefix}}TagCreate.md) |  | 

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
201 | [ApiResponseFor201](#create_tag_v2_tags_post.ApiResponseFor201) | The created tag
422 | [ApiResponseFor422](#create_tag_v2_tags_post.ApiResponseFor422) | Validation Error

#### create_tag_v2_tags_post.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Tag**](../../models/Tag.md) |  | 


#### create_tag_v2_tags_post.ApiResponseFor422
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

# **create_tag_v2_tags_post_0**
<a name="create_tag_v2_tags_post_0"></a>
> Tag create_tag_v2_tags_post_0(any_type)

Create tag

Create a tag

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
from versify.model.tag import Tag
from versify.model.http_validation_error import HTTPValidationError
from versify.model.tag_create import TagCreate
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Create tag
        api_response = api_instance.create_tag_v2_tags_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->create_tag_v2_tags_post_0: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Create tag
        api_response = api_instance.create_tag_v2_tags_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->create_tag_v2_tags_post_0: %s\n" % e)
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
[TagCreate]({{complexTypePrefix}}TagCreate.md) | [**TagCreate**]({{complexTypePrefix}}TagCreate.md) | [**TagCreate**]({{complexTypePrefix}}TagCreate.md) |  | 

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
201 | [ApiResponseFor201](#create_tag_v2_tags_post_0.ApiResponseFor201) | The created tag
422 | [ApiResponseFor422](#create_tag_v2_tags_post_0.ApiResponseFor422) | Validation Error

#### create_tag_v2_tags_post_0.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Tag**](../../models/Tag.md) |  | 


#### create_tag_v2_tags_post_0.ApiResponseFor422
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

# **delete_tag_v2_tags_tag_id_delete**
<a name="delete_tag_v2_tags_tag_id_delete"></a>
> ApiDeleteResponse delete_tag_v2_tags_tag_id_delete(tag_id)

Delete tag

Delete an tag

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Delete tag
        api_response = api_instance.delete_tag_v2_tags_tag_id_delete(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->delete_tag_v2_tags_tag_id_delete: %s\n" % e)

    # example passing only optional values
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Delete tag
        api_response = api_instance.delete_tag_v2_tags_tag_id_delete(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->delete_tag_v2_tags_tag_id_delete: %s\n" % e)
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
tag_id | TagIdSchema | | 

# TagIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_tag_v2_tags_tag_id_delete.ApiResponseFor200) | The deleted tag
422 | [ApiResponseFor422](#delete_tag_v2_tags_tag_id_delete.ApiResponseFor422) | Validation Error

#### delete_tag_v2_tags_tag_id_delete.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiDeleteResponse**](../../models/ApiDeleteResponse.md) |  | 


#### delete_tag_v2_tags_tag_id_delete.ApiResponseFor422
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

# **delete_tag_v2_tags_tag_id_delete_0**
<a name="delete_tag_v2_tags_tag_id_delete_0"></a>
> ApiDeleteResponse delete_tag_v2_tags_tag_id_delete_0(tag_id)

Delete tag

Delete an tag

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Delete tag
        api_response = api_instance.delete_tag_v2_tags_tag_id_delete_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->delete_tag_v2_tags_tag_id_delete_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Delete tag
        api_response = api_instance.delete_tag_v2_tags_tag_id_delete_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->delete_tag_v2_tags_tag_id_delete_0: %s\n" % e)
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
tag_id | TagIdSchema | | 

# TagIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_tag_v2_tags_tag_id_delete_0.ApiResponseFor200) | The deleted tag
422 | [ApiResponseFor422](#delete_tag_v2_tags_tag_id_delete_0.ApiResponseFor422) | Validation Error

#### delete_tag_v2_tags_tag_id_delete_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiDeleteResponse**](../../models/ApiDeleteResponse.md) |  | 


#### delete_tag_v2_tags_tag_id_delete_0.ApiResponseFor422
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

# **get_tag_v2_tags_tag_id_get**
<a name="get_tag_v2_tags_tag_id_get"></a>
> Tag get_tag_v2_tags_tag_id_get(tag_id)

Get tag

Get a tag

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
from versify.model.tag import Tag
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Get tag
        api_response = api_instance.get_tag_v2_tags_tag_id_get(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->get_tag_v2_tags_tag_id_get: %s\n" % e)

    # example passing only optional values
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Get tag
        api_response = api_instance.get_tag_v2_tags_tag_id_get(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->get_tag_v2_tags_tag_id_get: %s\n" % e)
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
tag_id | TagIdSchema | | 

# TagIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_tag_v2_tags_tag_id_get.ApiResponseFor200) | The tag
422 | [ApiResponseFor422](#get_tag_v2_tags_tag_id_get.ApiResponseFor422) | Validation Error

#### get_tag_v2_tags_tag_id_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Tag**](../../models/Tag.md) |  | 


#### get_tag_v2_tags_tag_id_get.ApiResponseFor422
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

# **get_tag_v2_tags_tag_id_get_0**
<a name="get_tag_v2_tags_tag_id_get_0"></a>
> Tag get_tag_v2_tags_tag_id_get_0(tag_id)

Get tag

Get a tag

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
from versify.model.tag import Tag
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Get tag
        api_response = api_instance.get_tag_v2_tags_tag_id_get_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->get_tag_v2_tags_tag_id_get_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Get tag
        api_response = api_instance.get_tag_v2_tags_tag_id_get_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->get_tag_v2_tags_tag_id_get_0: %s\n" % e)
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
tag_id | TagIdSchema | | 

# TagIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_tag_v2_tags_tag_id_get_0.ApiResponseFor200) | The tag
422 | [ApiResponseFor422](#get_tag_v2_tags_tag_id_get_0.ApiResponseFor422) | Validation Error

#### get_tag_v2_tags_tag_id_get_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Tag**](../../models/Tag.md) |  | 


#### get_tag_v2_tags_tag_id_get_0.ApiResponseFor422
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

# **list_tags_v2_tags_get**
<a name="list_tags_v2_tags_get"></a>
> ApiListResponse list_tags_v2_tags_get()

List tags

List tags with optional filters and pagination parameters

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
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
    api_instance = tags_api.TagsApi(api_client)

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
        # List tags
        api_response = api_instance.list_tags_v2_tags_get(
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->list_tags_v2_tags_get: %s\n" % e)
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
200 | [ApiResponseFor200](#list_tags_v2_tags_get.ApiResponseFor200) | The list of tags
422 | [ApiResponseFor422](#list_tags_v2_tags_get.ApiResponseFor422) | Validation Error

#### list_tags_v2_tags_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiListResponse**](../../models/ApiListResponse.md) |  | 


#### list_tags_v2_tags_get.ApiResponseFor422
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

# **list_tags_v2_tags_get_0**
<a name="list_tags_v2_tags_get_0"></a>
> ApiListResponse list_tags_v2_tags_get_0()

List tags

List tags with optional filters and pagination parameters

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
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
    api_instance = tags_api.TagsApi(api_client)

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
        # List tags
        api_response = api_instance.list_tags_v2_tags_get_0(
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->list_tags_v2_tags_get_0: %s\n" % e)
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
200 | [ApiResponseFor200](#list_tags_v2_tags_get_0.ApiResponseFor200) | The list of tags
422 | [ApiResponseFor422](#list_tags_v2_tags_get_0.ApiResponseFor422) | Validation Error

#### list_tags_v2_tags_get_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiListResponse**](../../models/ApiListResponse.md) |  | 


#### list_tags_v2_tags_get_0.ApiResponseFor422
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

# **search_tags_v2_tags_search_post**
<a name="search_tags_v2_tags_search_post"></a>
> ApiSearchResponse search_tags_v2_tags_search_post(any_type)

Search tags

Search tags with query string

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Search tags
        api_response = api_instance.search_tags_v2_tags_search_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->search_tags_v2_tags_search_post: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Search tags
        api_response = api_instance.search_tags_v2_tags_search_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->search_tags_v2_tags_search_post: %s\n" % e)
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
200 | [ApiResponseFor200](#search_tags_v2_tags_search_post.ApiResponseFor200) | The list of tags
422 | [ApiResponseFor422](#search_tags_v2_tags_search_post.ApiResponseFor422) | Validation Error

#### search_tags_v2_tags_search_post.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiSearchResponse**](../../models/ApiSearchResponse.md) |  | 


#### search_tags_v2_tags_search_post.ApiResponseFor422
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

# **search_tags_v2_tags_search_post_0**
<a name="search_tags_v2_tags_search_post_0"></a>
> ApiSearchResponse search_tags_v2_tags_search_post_0(any_type)

Search tags

Search tags with query string

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Search tags
        api_response = api_instance.search_tags_v2_tags_search_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->search_tags_v2_tags_search_post_0: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Search tags
        api_response = api_instance.search_tags_v2_tags_search_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->search_tags_v2_tags_search_post_0: %s\n" % e)
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
200 | [ApiResponseFor200](#search_tags_v2_tags_search_post_0.ApiResponseFor200) | The list of tags
422 | [ApiResponseFor422](#search_tags_v2_tags_search_post_0.ApiResponseFor422) | Validation Error

#### search_tags_v2_tags_search_post_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiSearchResponse**](../../models/ApiSearchResponse.md) |  | 


#### search_tags_v2_tags_search_post_0.ApiResponseFor422
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

# **update_tag_v2_tags_tag_id_put**
<a name="update_tag_v2_tags_tag_id_put"></a>
> Tag update_tag_v2_tags_tag_id_put(tag_idany_type)

Update tag

Update an tag

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
from versify.model.tag import Tag
from versify.model.tag_update import TagUpdate
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
    }
    body = None
    try:
        # Update tag
        api_response = api_instance.update_tag_v2_tags_tag_id_put(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->update_tag_v2_tags_tag_id_put: %s\n" % e)

    # example passing only optional values
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Update tag
        api_response = api_instance.update_tag_v2_tags_tag_id_put(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->update_tag_v2_tags_tag_id_put: %s\n" % e)
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
[TagUpdate]({{complexTypePrefix}}TagUpdate.md) | [**TagUpdate**]({{complexTypePrefix}}TagUpdate.md) | [**TagUpdate**]({{complexTypePrefix}}TagUpdate.md) |  | 

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
tag_id | TagIdSchema | | 

# TagIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_tag_v2_tags_tag_id_put.ApiResponseFor200) | The updated tag
422 | [ApiResponseFor422](#update_tag_v2_tags_tag_id_put.ApiResponseFor422) | Validation Error

#### update_tag_v2_tags_tag_id_put.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Tag**](../../models/Tag.md) |  | 


#### update_tag_v2_tags_tag_id_put.ApiResponseFor422
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

# **update_tag_v2_tags_tag_id_put_0**
<a name="update_tag_v2_tags_tag_id_put_0"></a>
> Tag update_tag_v2_tags_tag_id_put_0(tag_idany_type)

Update tag

Update an tag

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import tags_api
from versify.model.tag import Tag
from versify.model.tag_update import TagUpdate
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
    api_instance = tags_api.TagsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
    }
    body = None
    try:
        # Update tag
        api_response = api_instance.update_tag_v2_tags_tag_id_put_0(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->update_tag_v2_tags_tag_id_put_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'tag_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Update tag
        api_response = api_instance.update_tag_v2_tags_tag_id_put_0(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling TagsApi->update_tag_v2_tags_tag_id_put_0: %s\n" % e)
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
[TagUpdate]({{complexTypePrefix}}TagUpdate.md) | [**TagUpdate**]({{complexTypePrefix}}TagUpdate.md) | [**TagUpdate**]({{complexTypePrefix}}TagUpdate.md) |  | 

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
tag_id | TagIdSchema | | 

# TagIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_tag_v2_tags_tag_id_put_0.ApiResponseFor200) | The updated tag
422 | [ApiResponseFor422](#update_tag_v2_tags_tag_id_put_0.ApiResponseFor422) | Validation Error

#### update_tag_v2_tags_tag_id_put_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Tag**](../../models/Tag.md) |  | 


#### update_tag_v2_tags_tag_id_put_0.ApiResponseFor422
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

