<a name="__pageTop"></a>
# versify.apis.tags.claims_api.ClaimsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_claim_v2_claims_post**](#create_claim_v2_claims_post) | **post** /v2/claims | Create claim
[**create_claim_v2_claims_post_0**](#create_claim_v2_claims_post_0) | **post** /v2/claims | Create claim
[**delete_claim_v2_claims_claim_id_delete**](#delete_claim_v2_claims_claim_id_delete) | **delete** /v2/claims/{claim_id} | Delete claim
[**delete_claim_v2_claims_claim_id_delete_0**](#delete_claim_v2_claims_claim_id_delete_0) | **delete** /v2/claims/{claim_id} | Delete claim
[**get_claim_v2_claims_claim_id_get**](#get_claim_v2_claims_claim_id_get) | **get** /v2/claims/{claim_id} | Get claim
[**get_claim_v2_claims_claim_id_get_0**](#get_claim_v2_claims_claim_id_get_0) | **get** /v2/claims/{claim_id} | Get claim
[**list_claims_v2_claims_get**](#list_claims_v2_claims_get) | **get** /v2/claims | List claims
[**list_claims_v2_claims_get_0**](#list_claims_v2_claims_get_0) | **get** /v2/claims | List claims
[**search_claims_v2_claims_search_post**](#search_claims_v2_claims_search_post) | **post** /v2/claims/search | Search claims
[**search_claims_v2_claims_search_post_0**](#search_claims_v2_claims_search_post_0) | **post** /v2/claims/search | Search claims
[**update_claim_v2_claims_claim_id_put**](#update_claim_v2_claims_claim_id_put) | **put** /v2/claims/{claim_id} | Update claim
[**update_claim_v2_claims_claim_id_put_0**](#update_claim_v2_claims_claim_id_put_0) | **put** /v2/claims/{claim_id} | Update claim

# **create_claim_v2_claims_post**
<a name="create_claim_v2_claims_post"></a>
> Claim create_claim_v2_claims_post(any_type)

Create claim

Create a claim

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
from versify.model.claim import Claim
from versify.model.claim_create import ClaimCreate
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Create claim
        api_response = api_instance.create_claim_v2_claims_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->create_claim_v2_claims_post: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Create claim
        api_response = api_instance.create_claim_v2_claims_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->create_claim_v2_claims_post: %s\n" % e)
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
[ClaimCreate]({{complexTypePrefix}}ClaimCreate.md) | [**ClaimCreate**]({{complexTypePrefix}}ClaimCreate.md) | [**ClaimCreate**]({{complexTypePrefix}}ClaimCreate.md) |  | 

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
201 | [ApiResponseFor201](#create_claim_v2_claims_post.ApiResponseFor201) | The created claim
422 | [ApiResponseFor422](#create_claim_v2_claims_post.ApiResponseFor422) | Validation Error

#### create_claim_v2_claims_post.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Claim**](../../models/Claim.md) |  | 


#### create_claim_v2_claims_post.ApiResponseFor422
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

# **create_claim_v2_claims_post_0**
<a name="create_claim_v2_claims_post_0"></a>
> Claim create_claim_v2_claims_post_0(any_type)

Create claim

Create a claim

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
from versify.model.claim import Claim
from versify.model.claim_create import ClaimCreate
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Create claim
        api_response = api_instance.create_claim_v2_claims_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->create_claim_v2_claims_post_0: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Create claim
        api_response = api_instance.create_claim_v2_claims_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->create_claim_v2_claims_post_0: %s\n" % e)
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
[ClaimCreate]({{complexTypePrefix}}ClaimCreate.md) | [**ClaimCreate**]({{complexTypePrefix}}ClaimCreate.md) | [**ClaimCreate**]({{complexTypePrefix}}ClaimCreate.md) |  | 

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
201 | [ApiResponseFor201](#create_claim_v2_claims_post_0.ApiResponseFor201) | The created claim
422 | [ApiResponseFor422](#create_claim_v2_claims_post_0.ApiResponseFor422) | Validation Error

#### create_claim_v2_claims_post_0.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Claim**](../../models/Claim.md) |  | 


#### create_claim_v2_claims_post_0.ApiResponseFor422
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

# **delete_claim_v2_claims_claim_id_delete**
<a name="delete_claim_v2_claims_claim_id_delete"></a>
> ApiDeleteResponse delete_claim_v2_claims_claim_id_delete(claim_id)

Delete claim

Delete an claim

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Delete claim
        api_response = api_instance.delete_claim_v2_claims_claim_id_delete(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->delete_claim_v2_claims_claim_id_delete: %s\n" % e)

    # example passing only optional values
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Delete claim
        api_response = api_instance.delete_claim_v2_claims_claim_id_delete(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->delete_claim_v2_claims_claim_id_delete: %s\n" % e)
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
claim_id | ClaimIdSchema | | 

# ClaimIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_claim_v2_claims_claim_id_delete.ApiResponseFor200) | The deleted claim
422 | [ApiResponseFor422](#delete_claim_v2_claims_claim_id_delete.ApiResponseFor422) | Validation Error

#### delete_claim_v2_claims_claim_id_delete.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiDeleteResponse**](../../models/ApiDeleteResponse.md) |  | 


#### delete_claim_v2_claims_claim_id_delete.ApiResponseFor422
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

# **delete_claim_v2_claims_claim_id_delete_0**
<a name="delete_claim_v2_claims_claim_id_delete_0"></a>
> ApiDeleteResponse delete_claim_v2_claims_claim_id_delete_0(claim_id)

Delete claim

Delete an claim

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Delete claim
        api_response = api_instance.delete_claim_v2_claims_claim_id_delete_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->delete_claim_v2_claims_claim_id_delete_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Delete claim
        api_response = api_instance.delete_claim_v2_claims_claim_id_delete_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->delete_claim_v2_claims_claim_id_delete_0: %s\n" % e)
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
claim_id | ClaimIdSchema | | 

# ClaimIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#delete_claim_v2_claims_claim_id_delete_0.ApiResponseFor200) | The deleted claim
422 | [ApiResponseFor422](#delete_claim_v2_claims_claim_id_delete_0.ApiResponseFor422) | Validation Error

#### delete_claim_v2_claims_claim_id_delete_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiDeleteResponse**](../../models/ApiDeleteResponse.md) |  | 


#### delete_claim_v2_claims_claim_id_delete_0.ApiResponseFor422
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

# **get_claim_v2_claims_claim_id_get**
<a name="get_claim_v2_claims_claim_id_get"></a>
> Claim get_claim_v2_claims_claim_id_get(claim_id)

Get claim

Get a claim

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
from versify.model.claim import Claim
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Get claim
        api_response = api_instance.get_claim_v2_claims_claim_id_get(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->get_claim_v2_claims_claim_id_get: %s\n" % e)

    # example passing only optional values
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Get claim
        api_response = api_instance.get_claim_v2_claims_claim_id_get(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->get_claim_v2_claims_claim_id_get: %s\n" % e)
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
claim_id | ClaimIdSchema | | 

# ClaimIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_claim_v2_claims_claim_id_get.ApiResponseFor200) | The claim
422 | [ApiResponseFor422](#get_claim_v2_claims_claim_id_get.ApiResponseFor422) | Validation Error

#### get_claim_v2_claims_claim_id_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Claim**](../../models/Claim.md) |  | 


#### get_claim_v2_claims_claim_id_get.ApiResponseFor422
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

# **get_claim_v2_claims_claim_id_get_0**
<a name="get_claim_v2_claims_claim_id_get_0"></a>
> Claim get_claim_v2_claims_claim_id_get_0(claim_id)

Get claim

Get a claim

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
from versify.model.claim import Claim
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
    }
    try:
        # Get claim
        api_response = api_instance.get_claim_v2_claims_claim_id_get_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->get_claim_v2_claims_claim_id_get_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    try:
        # Get claim
        api_response = api_instance.get_claim_v2_claims_claim_id_get_0(
            path_params=path_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->get_claim_v2_claims_claim_id_get_0: %s\n" % e)
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
claim_id | ClaimIdSchema | | 

# ClaimIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_claim_v2_claims_claim_id_get_0.ApiResponseFor200) | The claim
422 | [ApiResponseFor422](#get_claim_v2_claims_claim_id_get_0.ApiResponseFor422) | Validation Error

#### get_claim_v2_claims_claim_id_get_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Claim**](../../models/Claim.md) |  | 


#### get_claim_v2_claims_claim_id_get_0.ApiResponseFor422
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

# **list_claims_v2_claims_get**
<a name="list_claims_v2_claims_get"></a>
> ApiListResponse list_claims_v2_claims_get()

List claims

List claims with optional filters and pagination parameters

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
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
    api_instance = claims_api.ClaimsApi(api_client)

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
        # List claims
        api_response = api_instance.list_claims_v2_claims_get(
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->list_claims_v2_claims_get: %s\n" % e)
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
200 | [ApiResponseFor200](#list_claims_v2_claims_get.ApiResponseFor200) | The list of claims
422 | [ApiResponseFor422](#list_claims_v2_claims_get.ApiResponseFor422) | Validation Error

#### list_claims_v2_claims_get.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiListResponse**](../../models/ApiListResponse.md) |  | 


#### list_claims_v2_claims_get.ApiResponseFor422
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

# **list_claims_v2_claims_get_0**
<a name="list_claims_v2_claims_get_0"></a>
> ApiListResponse list_claims_v2_claims_get_0()

List claims

List claims with optional filters and pagination parameters

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
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
    api_instance = claims_api.ClaimsApi(api_client)

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
        # List claims
        api_response = api_instance.list_claims_v2_claims_get_0(
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->list_claims_v2_claims_get_0: %s\n" % e)
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
200 | [ApiResponseFor200](#list_claims_v2_claims_get_0.ApiResponseFor200) | The list of claims
422 | [ApiResponseFor422](#list_claims_v2_claims_get_0.ApiResponseFor422) | Validation Error

#### list_claims_v2_claims_get_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiListResponse**](../../models/ApiListResponse.md) |  | 


#### list_claims_v2_claims_get_0.ApiResponseFor422
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

# **search_claims_v2_claims_search_post**
<a name="search_claims_v2_claims_search_post"></a>
> ApiSearchResponse search_claims_v2_claims_search_post(any_type)

Search claims

Search claims with query string

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Search claims
        api_response = api_instance.search_claims_v2_claims_search_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->search_claims_v2_claims_search_post: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Search claims
        api_response = api_instance.search_claims_v2_claims_search_post(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->search_claims_v2_claims_search_post: %s\n" % e)
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
200 | [ApiResponseFor200](#search_claims_v2_claims_search_post.ApiResponseFor200) | The list of claims
422 | [ApiResponseFor422](#search_claims_v2_claims_search_post.ApiResponseFor422) | Validation Error

#### search_claims_v2_claims_search_post.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiSearchResponse**](../../models/ApiSearchResponse.md) |  | 


#### search_claims_v2_claims_search_post.ApiResponseFor422
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

# **search_claims_v2_claims_search_post_0**
<a name="search_claims_v2_claims_search_post_0"></a>
> ApiSearchResponse search_claims_v2_claims_search_post_0(any_type)

Search claims

Search claims with query string

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    header_params = {
    }
    body = None
    try:
        # Search claims
        api_response = api_instance.search_claims_v2_claims_search_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->search_claims_v2_claims_search_post_0: %s\n" % e)

    # example passing only optional values
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Search claims
        api_response = api_instance.search_claims_v2_claims_search_post_0(
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->search_claims_v2_claims_search_post_0: %s\n" % e)
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
200 | [ApiResponseFor200](#search_claims_v2_claims_search_post_0.ApiResponseFor200) | The list of claims
422 | [ApiResponseFor422](#search_claims_v2_claims_search_post_0.ApiResponseFor422) | Validation Error

#### search_claims_v2_claims_search_post_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**ApiSearchResponse**](../../models/ApiSearchResponse.md) |  | 


#### search_claims_v2_claims_search_post_0.ApiResponseFor422
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

# **update_claim_v2_claims_claim_id_put**
<a name="update_claim_v2_claims_claim_id_put"></a>
> Claim update_claim_v2_claims_claim_id_put(claim_idany_type)

Update claim

Update an claim

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
from versify.model.claim_update import ClaimUpdate
from versify.model.claim import Claim
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
    }
    body = None
    try:
        # Update claim
        api_response = api_instance.update_claim_v2_claims_claim_id_put(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->update_claim_v2_claims_claim_id_put: %s\n" % e)

    # example passing only optional values
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Update claim
        api_response = api_instance.update_claim_v2_claims_claim_id_put(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->update_claim_v2_claims_claim_id_put: %s\n" % e)
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
[ClaimUpdate]({{complexTypePrefix}}ClaimUpdate.md) | [**ClaimUpdate**]({{complexTypePrefix}}ClaimUpdate.md) | [**ClaimUpdate**]({{complexTypePrefix}}ClaimUpdate.md) |  | 

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
claim_id | ClaimIdSchema | | 

# ClaimIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_claim_v2_claims_claim_id_put.ApiResponseFor200) | The updated claim
422 | [ApiResponseFor422](#update_claim_v2_claims_claim_id_put.ApiResponseFor422) | Validation Error

#### update_claim_v2_claims_claim_id_put.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Claim**](../../models/Claim.md) |  | 


#### update_claim_v2_claims_claim_id_put.ApiResponseFor422
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

# **update_claim_v2_claims_claim_id_put_0**
<a name="update_claim_v2_claims_claim_id_put_0"></a>
> Claim update_claim_v2_claims_claim_id_put_0(claim_idany_type)

Update claim

Update an claim

### Example

* Bearer Authentication (HTTPBearer):
```python
import versify
from versify.apis.tags import claims_api
from versify.model.claim_update import ClaimUpdate
from versify.model.claim import Claim
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
    api_instance = claims_api.ClaimsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
    }
    body = None
    try:
        # Update claim
        api_response = api_instance.update_claim_v2_claims_claim_id_put_0(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->update_claim_v2_claims_claim_id_put_0: %s\n" % e)

    # example passing only optional values
    path_params = {
        'claim_id': "con_12121231231231321",
    }
    header_params = {
        'Versify-Account': "act_123123123131231231",
    }
    body = None
    try:
        # Update claim
        api_response = api_instance.update_claim_v2_claims_claim_id_put_0(
            path_params=path_params,
            header_params=header_params,
            body=body,
        )
        pprint(api_response)
    except versify.ApiException as e:
        print("Exception when calling ClaimsApi->update_claim_v2_claims_claim_id_put_0: %s\n" % e)
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
[ClaimUpdate]({{complexTypePrefix}}ClaimUpdate.md) | [**ClaimUpdate**]({{complexTypePrefix}}ClaimUpdate.md) | [**ClaimUpdate**]({{complexTypePrefix}}ClaimUpdate.md) |  | 

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
claim_id | ClaimIdSchema | | 

# ClaimIdSchema

Unique identifier of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Unique identifier of the contact | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_claim_v2_claims_claim_id_put_0.ApiResponseFor200) | The updated claim
422 | [ApiResponseFor422](#update_claim_v2_claims_claim_id_put_0.ApiResponseFor422) | Validation Error

#### update_claim_v2_claims_claim_id_put_0.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**Claim**](../../models/Claim.md) |  | 


#### update_claim_v2_claims_claim_id_put_0.ApiResponseFor422
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

