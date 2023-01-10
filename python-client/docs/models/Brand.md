# versify.model.brand.Brand

A brand used to customize the look and feel of an account.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A brand used to customize the look and feel of an account. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**action_color** | str,  | str,  | The action color of the brand | [optional] if omitted the server will use the default value of "#000000"
**background_color** | str,  | str,  | The background color of the brand | [optional] if omitted the server will use the default value of "#000000"
**logo** | str,  | str,  | The URL of the brand&#x27;s logo | [optional] 
**primary_color** | str,  | str,  | The primary color of the brand | [optional] if omitted the server will use the default value of "#000000"
**secondary_color** | str,  | str,  | The secondary color of the brand | [optional] if omitted the server will use the default value of "#000000"
**tertiary_color** | str,  | str,  | The tertiary color of the brand | [optional] if omitted the server will use the default value of "#000000"
**wallet_action_color** | str,  | str,  | The wallet action color of the brand | [optional] if omitted the server will use the default value of "#000000"
**wallet_background_color** | str,  | str,  | The wallet background color of the brand | [optional] if omitted the server will use the default value of "#000000"
**[wallet_display_filters](#wallet_display_filters)** | list, tuple,  | tuple,  | The wallet display filters of the brand | [optional] 
**[wallet_position](#wallet_position)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The wallet position of the brand | [optional] if omitted the server will use the default value of bottom-left
**wallet_welcome_message** | str,  | str,  | The wallet welcome message of the brand | [optional] if omitted the server will use the default value of "Welcome"
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# wallet_display_filters

The wallet display filters of the brand

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | The wallet display filters of the brand | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Query**](Query.md) | [**Query**](Query.md) | [**Query**](Query.md) |  | 

# wallet_position

The wallet position of the brand

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The wallet position of the brand | if omitted the server will use the default value of bottom-left

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[WalletPosition](WalletPosition.md) | [**WalletPosition**](WalletPosition.md) | [**WalletPosition**](WalletPosition.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

