# versify.model.user.User

A user document in the database.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A user document in the database. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**avatar** | str,  | str,  | The URL of the user&#x27;s avatar | 
**email** | str,  | str,  | The email address of the user | 
**_id** | str,  | str,  | Unique identifier for the user | [optional] 
**active** | bool,  | BoolClass,  | Whether the user is active | [optional] if omitted the server will use the default value of True
**created** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was created | [optional] 
**email_verified** | bool,  | BoolClass,  | Whether the user&#x27;s email address has been verified | [optional] if omitted the server will use the default value of False
**[metadata](#metadata)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | [optional] if omitted the server will use the default value of {}
**[name](#name)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The name of the user | [optional] if omitted the server will use the default value of {}
**object** | str,  | str,  | The object type. Always \&quot;user\&quot; | [optional] if omitted the server will use the default value of "user"
**phone_number** | str,  | str,  | The phone number of the user | [optional] 
**phone_number_verified** | bool,  | BoolClass,  | Whether the user&#x27;s phone number has been verified | [optional] if omitted the server will use the default value of False
**[providers](#providers)** | list, tuple,  | tuple,  | The identity providers the user belongs to | [optional] 
**updated** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was last updated | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# metadata

Arbitrary metadata associated with the object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | if omitted the server will use the default value of {}

# name

The name of the user

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The name of the user | if omitted the server will use the default value of {}

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[PersonName](PersonName.md) | [**PersonName**](PersonName.md) | [**PersonName**](PersonName.md) |  | 

# providers

The identity providers the user belongs to

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The identity providers the user belongs to | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**IdentityProvider**](IdentityProvider.md) | [**IdentityProvider**](IdentityProvider.md) | [**IdentityProvider**](IdentityProvider.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

