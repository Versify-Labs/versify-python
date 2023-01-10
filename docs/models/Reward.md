# versify.model.reward.Reward

A reward document in the database.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A reward document in the database. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**asset** | str,  | str,  | The asset the reward is for | 
**account** | str,  | str,  | The account the reward belongs to | 
**_id** | str,  | str,  | Unique identifier for the reward | [optional] 
**active** | bool,  | BoolClass,  | Whether the reward is active | [optional] if omitted the server will use the default value of True
**asset_quantity** | decimal.Decimal, int,  | decimal.Decimal,  | The quantity of the asset needed to redeem the reward | [optional] if omitted the server will use the default value of 1
**created** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was created | [optional] 
**description** | str,  | str,  | The description of the reward | [optional] if omitted the server will use the default value of ""
**image** | str,  | str,  | The image of the reward | [optional] 
**[metadata](#metadata)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | [optional] if omitted the server will use the default value of {}
**name** | str,  | str,  | The name of the reward. This is displayable to the customer. | [optional] if omitted the server will use the default value of "Reward"
**object** | str,  | str,  | The object type. Always \&quot;reward\&quot; | [optional] if omitted the server will use the default value of "reward"
**[reward_type](#reward_type)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The type of the reward | [optional] if omitted the server will use the default value of coupon
**updated** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was last updated | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# metadata

Arbitrary metadata associated with the object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | if omitted the server will use the default value of {}

# reward_type

The type of the reward

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | The type of the reward | if omitted the server will use the default value of coupon

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[RewardType](RewardType.md) | [**RewardType**](RewardType.md) | [**RewardType**](RewardType.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

