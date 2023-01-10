# versify.model.journey.Journey

A journey document in the database.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A journey document in the database. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**name** | str,  | str,  | The name of the journey. Internal facing. | 
**[trigger](#trigger)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The trigger for the journey | 
**account** | str,  | str,  | The account the journey belongs to | 
**_id** | str,  | str,  | Unique identifier for the journey | [optional] 
**active** | bool,  | BoolClass,  | Whether the journey is active | [optional] if omitted the server will use the default value of True
**created** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was created | [optional] 
**description** | str,  | str,  | A description of the journey | [optional] if omitted the server will use the default value of ""
**[metadata](#metadata)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | [optional] if omitted the server will use the default value of {}
**object** | str,  | str,  | The object type. Always \&quot;journey\&quot; | [optional] if omitted the server will use the default value of "journey"
**start** | str,  | str,  | The starting state of the journey | [optional] if omitted the server will use the default value of "start"
**[states](#states)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | The states of the journey | [optional] 
**updated** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was last updated | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# trigger

The trigger for the journey

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The trigger for the journey | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[Trigger](Trigger.md) | [**Trigger**](Trigger.md) | [**Trigger**](Trigger.md) |  | 

# metadata

Arbitrary metadata associated with the object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | if omitted the server will use the default value of {}

# states

The states of the journey

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | The states of the journey | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**Action**](Action.md) | [**Action**](Action.md) | any string name can be used but the value must be the correct type | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

