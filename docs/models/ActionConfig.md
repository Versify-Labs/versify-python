# versify.model.action_config.ActionConfig

An action configuration.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | An action configuration. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**asset** | str,  | str,  | The asset to send | [optional] 
**body** | str,  | str,  | The body of the message | [optional] 
**[filters](#filters)** | list, tuple,  | tuple,  | The filters to match | [optional] 
**member** | str,  | str,  | The member to send the message to | [optional] 
**message_type** | str,  | str,  | The type of the message | [optional] 
**note** | str,  | str,  | The note to create | [optional] 
**quantity** | decimal.Decimal, int,  | decimal.Decimal,  | The quantity of the reward | [optional] 
**seconds** | decimal.Decimal, int,  | decimal.Decimal,  | The number of seconds to wait | [optional] 
**subject** | str,  | str,  | The subject of the message | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | The tags to add to the contact | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# filters

The filters to match

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The filters to match | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Query**](Query.md) | [**Query**](Query.md) | [**Query**](Query.md) |  | 

# tags

The tags to add to the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The tags to add to the contact | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

