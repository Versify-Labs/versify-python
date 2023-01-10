# versify.model.collection.Collection

A collection document in the database.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A collection document in the database. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**name** | str,  | str,  | The name of the collection | 
**account** | str,  | str,  | The account the collection belongs to | 
**_id** | str,  | str,  | Unique identifier for the collection | [optional] 
**contract_address** | str,  | str,  | The address of the contract | [optional] 
**created** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was created | [optional] 
**default** | bool,  | BoolClass,  | Whether this is the default collection | [optional] if omitted the server will use the default value of False
**description** | str,  | str,  | The description of the collection | [optional] 
**image** | str,  | str,  | The image of the collection | [optional] if omitted the server will use the default value of "https://cdn.versifylabs.com/branding/Logos/verisify-logo-transparent-bg.png"
**[metadata](#metadata)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | [optional] if omitted the server will use the default value of {}
**object** | str,  | str,  | The object type. Always \&quot;collection\&quot; | [optional] if omitted the server will use the default value of "collection"
**signature** | str,  | str,  | The signature of the collection | [optional] 
**status** | str,  | str,  | The status of the collection | [optional] if omitted the server will use the default value of "new"
**transaction** | str,  | str,  | The transaction of the collection | [optional] 
**updated** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was last updated | [optional] 
**uri** | str,  | str,  | The uri of the collection | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# metadata

Arbitrary metadata associated with the object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | if omitted the server will use the default value of {}

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

