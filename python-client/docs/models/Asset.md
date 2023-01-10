# versify.model.asset.Asset

A asset document in the database.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A asset document in the database. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**image** | str,  | str,  | The image of the asset | 
**token_id** | str,  | str,  | The token ID of the asset | 
**name** | str,  | str,  | The name of the asset. Displayed on third party apps. | 
**description** | str,  | str,  | The description of the asset | 
**collection** | str,  | str,  | The ID of the collection that the asset belongs to | 
**contract_address** | str,  | str,  | The contract address of the asset | 
**account** | str,  | str,  | The account the asset belongs to | 
**_id** | str,  | str,  | Unique identifier for the asset | [optional] 
**[chain](#chain)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The blockchain the asset is on | [optional] if omitted the server will use the default value of polygon
**created** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was created | [optional] 
**[metadata](#metadata)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | [optional] if omitted the server will use the default value of {}
**object** | str,  | str,  | The object type | [optional] if omitted the server will use the default value of "asset"
**[properties](#properties)** | list, tuple,  | tuple,  | The properties of the asset. Displayed on third party apps. | [optional] 
**[status](#status)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The status of the asset | [optional] if omitted the server will use the default value of active
**updated** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was last updated | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# chain

The blockchain the asset is on

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The blockchain the asset is on | if omitted the server will use the default value of polygon

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[BlockchainType](BlockchainType.md) | [**BlockchainType**](BlockchainType.md) | [**BlockchainType**](BlockchainType.md) |  | 

# metadata

Arbitrary metadata associated with the object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | if omitted the server will use the default value of {}

# properties

The properties of the asset. Displayed on third party apps.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The properties of the asset. Displayed on third party apps. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# status

The status of the asset

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The status of the asset | if omitted the server will use the default value of active

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AssetStatus](AssetStatus.md) | [**AssetStatus**](AssetStatus.md) | [**AssetStatus**](AssetStatus.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

