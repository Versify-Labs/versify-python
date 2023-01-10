# versify.model.api_search_response.ApiSearchResponse

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**count** | decimal.Decimal, int,  | decimal.Decimal,  | The number of items returned | [optional] if omitted the server will use the default value of 0
**[data](#data)** | list, tuple,  | tuple,  | The list of items that match the filters and pagination parameters. | [optional] 
**has_more** | bool,  | BoolClass,  | Whether there are more items to be returned | [optional] if omitted the server will use the default value of False
**object** | str,  | str,  | The object type | [optional] if omitted the server will use the default value of "search_result"
**url** | str,  | str,  | The URL of the search request | [optional] if omitted the server will use the default value of "/v1/items/search"
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

The list of items that match the filters and pagination parameters.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The list of items that match the filters and pagination parameters. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Account**](Account.md) | [**Account**](Account.md) | [**Account**](Account.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

