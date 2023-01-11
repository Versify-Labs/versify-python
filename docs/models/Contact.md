# versify.model.contact.Contact

A contact document in the database.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A contact document in the database. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**account** | str,  | str,  | The account the contact belongs to | 
**email** | str,  | str,  | The email address of the contact | 
**_id** | str,  | str,  | Unique identifier for the contact | [optional] 
**[address](#address)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The address of the contact | [optional] 
**avatar** | str,  | str,  | The URL of the contact&#x27;s avatar | [optional] 
**browser** | str,  | str,  | The browser used by the contact | [optional] 
**created** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was created | [optional] 
**last_seen** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the contact was last seen | [optional] 
**[metadata](#metadata)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | [optional] if omitted the server will use the default value of {}
**[name](#name)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The name of the contact. Includes first, middle and last name. | [optional] 
**object** | str,  | str,  | The object type. Always &#x27;contact&#x27; | [optional] if omitted the server will use the default value of "contact"
**owner** | str,  | str,  | The ID of the user who owns the contact | [optional] 
**phone_number** | str,  | str,  | The phone number of the contact | [optional] 
**[social_profiles](#social_profiles)** | list, tuple,  | tuple,  | The social profiles associated with the contact | [optional] 
**[status](#status)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The status of the contact | [optional] if omitted the server will use the default value of active
**updated** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was last updated | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# address

The address of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The address of the contact | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[Address](Address.md) | [**Address**](Address.md) | [**Address**](Address.md) |  | 

# metadata

Arbitrary metadata associated with the object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | if omitted the server will use the default value of {}

# name

The name of the contact. Includes first, middle and last name.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The name of the contact. Includes first, middle and last name. | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[PersonName](PersonName.md) | [**PersonName**](PersonName.md) | [**PersonName**](PersonName.md) |  | 

# social_profiles

The social profiles associated with the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The social profiles associated with the contact | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**SocialProfile**](SocialProfile.md) | [**SocialProfile**](SocialProfile.md) | [**SocialProfile**](SocialProfile.md) |  | 

# status

The status of the contact

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The status of the contact | if omitted the server will use the default value of active

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[ContactStatus](ContactStatus.md) | [**ContactStatus**](ContactStatus.md) | [**ContactStatus**](ContactStatus.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

