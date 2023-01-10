# versify.model.trigger_schedule_config.TriggerScheduleConfig

A trigger schedule configuration.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A trigger schedule configuration. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**at** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp to trigger the event at | [optional] 
**cron** | str,  | str,  | The cron expression to trigger the event at | [optional] 
**end** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp to stop triggering the event at | [optional] 
**rate** | str,  | str,  | The rate to trigger the event at | [optional] 
**start** | decimal.Decimal, int,  | decimal.Decimal,  | The timestamp to start triggering the event at | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

