# versify.model.redemption.Redemption

A redemption document in the database.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A redemption document in the database. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**reward** | str,  | str,  | The reward the redemption is for | 
**contact** | str,  | str,  | The ID of the contact redeeming the reward. | 
**account** | str,  | str,  | The account the redemption belongs to | 
**_id** | str,  | str,  | Unique identifier for the redemption | [optional] 
**coupon_code** | str,  | str,  | The coupon code used to redeem the reward | [optional] 
**created** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was created | [optional] 
**discount_amount** | decimal.Decimal, int,  | decimal.Decimal,  | The amount of the discount used to redeem the reward | [optional] 
**discount_code** | str,  | str,  | The discount code used to redeem the reward | [optional] 
**gift_amount** | decimal.Decimal, int,  | decimal.Decimal,  | The amount of the gift used to redeem the reward | [optional] 
**gift_code** | str,  | str,  | The gift code used to redeem the reward | [optional] 
**[metadata](#metadata)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | [optional] if omitted the server will use the default value of {}
**object** | str,  | str,  | The object type. Always \&quot;redemption\&quot; | [optional] if omitted the server will use the default value of "redemption"
**pass_barcode** | str,  | str,  | The barcode of the pass used to redeem the reward | [optional] 
**pass_platform** | str,  | str,  | The platform of the pass used to redeem the reward | [optional] 
**pass_serial_number** | str,  | str,  | The serial number of the pass used to redeem the reward | [optional] 
**updated** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp when the event was last updated | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# metadata

Arbitrary metadata associated with the object

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Arbitrary metadata associated with the object | if omitted the server will use the default value of {}

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

