# versify.model.message.Message

A message document in the database.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A message document in the database. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**account** | str,  | str,  | The account the message belongs to | 
**_id** | str,  | str,  | Unique identifier for the message | [optional] 
**[bcc_list](#bcc_list)** | list, tuple,  | tuple,  | The bcc list of the message | [optional] 
**[cc_list](#cc_list)** | list, tuple,  | tuple,  | The cc list of the message | [optional] 
**content_body** | str,  | str,  | The body of the message | [optional] if omitted the server will use the default value of ""
**content_preheader** | str,  | str,  | The preheader of the message | [optional] 
**content_subject** | str,  | str,  | The subject of the message | [optional] 
**created** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was created | [optional] 
**from_email** | str,  | str,  | The from email of the message | [optional] 
**from_name** | str,  | str,  | The from name of the message | [optional] 
**[message_type](#message_type)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The type of the message | [optional] if omitted the server will use the default value of email
**[metadata](#metadata)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | [optional] if omitted the server will use the default value of {}
**object** | str,  | str,  | The object type. Always \&quot;message\&quot; | [optional] if omitted the server will use the default value of "message"
**reply_to_email** | str,  | str,  | The reply to email of the message | [optional] 
**[status](#status)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The status of the message | [optional] if omitted the server will use the default value of draft
**to_contact** | str,  | str,  | The to contact of the message | [optional] 
**to_email** | str,  | str,  | The to email of the message | [optional] 
**to_name** | str,  | str,  | The to name of the message | [optional] 
**updated** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was last updated | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# bcc_list

The bcc list of the message

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The bcc list of the message | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# cc_list

The cc list of the message

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The cc list of the message | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# message_type

The type of the message

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The type of the message | if omitted the server will use the default value of email

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[MessageType](MessageType.md) | [**MessageType**](MessageType.md) | [**MessageType**](MessageType.md) |  | 

# metadata

Arbitrary metadata associated with the object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | if omitted the server will use the default value of {}

# status

The status of the message

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The status of the message | if omitted the server will use the default value of draft

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[MessageStatus](MessageStatus.md) | [**MessageStatus**](MessageStatus.md) | [**MessageStatus**](MessageStatus.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

