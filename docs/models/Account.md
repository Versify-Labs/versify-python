# versify.model.account.Account

A account document in the database.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A account document in the database. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**domain** | str,  | str,  | The domain of the account | 
**name** | str,  | str,  | The name of the account | 
**_id** | str,  | str,  | Unique identifier for the account | [optional] 
**[apps](#apps)** | list, tuple,  | tuple,  | The apps associated with the account | [optional] 
**[billing](#billing)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The billing settings of the account | [optional] if omitted the server will use the default value of {"stripe_customer_id":"cus_7aa8b01bbbfff1a897e4de76812cbde7","subscription_plan":"trial","subscription_status":"active"}
**[brand](#brand)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The branding settings of the account | [optional] if omitted the server will use the default value of {"action_color":"#000000","background_color":"#000000","primary_color":"#000000","secondary_color":"#000000","tertiary_color":"#000000","wallet_action_color":"#000000","wallet_background_color":"#000000","wallet_display_filters":[],"wallet_position":"bottom-left","wallet_welcome_message":"Welcome"}
**created** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was created | [optional] 
**[metadata](#metadata)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | [optional] if omitted the server will use the default value of {}
**object** | str,  | str,  | The object type | [optional] if omitted the server will use the default value of "account"
**[status](#status)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The status of the account | [optional] if omitted the server will use the default value of active
**[team](#team)** | list, tuple,  | tuple,  | The team members and associated roles of the account | [optional] 
**updated** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was last updated | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# apps

The apps associated with the account

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The apps associated with the account | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**App**](App.md) | [**App**](App.md) | [**App**](App.md) |  | 

# billing

The billing settings of the account

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The billing settings of the account | if omitted the server will use the default value of {"stripe_customer_id":"cus_7aa8b01bbbfff1a897e4de76812cbde7","subscription_plan":"trial","subscription_status":"active"}

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[Billing](Billing.md) | [**Billing**](Billing.md) | [**Billing**](Billing.md) |  | 

# brand

The branding settings of the account

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The branding settings of the account | if omitted the server will use the default value of {"action_color":"#000000","background_color":"#000000","primary_color":"#000000","secondary_color":"#000000","tertiary_color":"#000000","wallet_action_color":"#000000","wallet_background_color":"#000000","wallet_display_filters":[],"wallet_position":"bottom-left","wallet_welcome_message":"Welcome"}

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[Brand](Brand.md) | [**Brand**](Brand.md) | [**Brand**](Brand.md) |  | 

# metadata

Arbitrary metadata associated with the object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | if omitted the server will use the default value of {}

# status

The status of the account

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The status of the account | if omitted the server will use the default value of active

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AccountStatus](AccountStatus.md) | [**AccountStatus**](AccountStatus.md) | [**AccountStatus**](AccountStatus.md) |  | 

# team

The team members and associated roles of the account

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The team members and associated roles of the account | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**TeamMember**](TeamMember.md) | [**TeamMember**](TeamMember.md) | [**TeamMember**](TeamMember.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

