# versify.model.asset_update.AssetUpdate

Base Serializer class.  Almost ALWAYS should be used in conjunction with `fastapi_contrib.serializers.openapi.patch` decorator to correctly handle inherited model fields and OpenAPI Schema generation with `response_model`.  Responsible for sanitizing data & converting JSON to & from MongoDBModel.  Contains supplemental function, related to MongoDBModel, mostly proxied to corresponding functions inside model (ex. save, update)  Heavily uses `Meta` class for fine-tuning input & output. Main fields are:     * exclude - set of fields that are excluded when serializing to dict                 and sanitizing list of dicts     * model - class of the MongoDBModel to use, inherits fields from it     * write_only_fields - set of fields that can be accepted in request,                           but excluded when serializing to dict     * read_only_fields - set of fields that cannot be accepted in request,                           but included when serializing to dict  Example usage:  .. code-block:: python      app = FastAPI()       class SomeModel(MongoDBModel):         field1: str       @openapi.patch     class SomeSerializer(Serializer):         read_only1: str = \"const\"         write_only2: int         not_visible: str = \"42\"          class Meta:             model = SomeModel             exclude = {\"not_visible\"}             write_only_fields = {\"write_only2\"}             read_only_fields = {\"read_only1\"}       @app.get(\"/\", response_model=SomeSerializer.response_model)     async def root(serializer: SomeSerializer):         model_instance = await serializer.save()         return model_instance.dict()  POST-ing to this route following JSON:  .. code-block:: json      {\"read_only1\": \"a\", \"write_only2\": 123, \"field1\": \"b\"}  Should return following response:  .. code-block:: json      {\"id\": 1, \"field1\": \"b\", \"read_only1\": \"const\"}

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Base Serializer class.  Almost ALWAYS should be used in conjunction with &#x60;fastapi_contrib.serializers.openapi.patch&#x60; decorator to correctly handle inherited model fields and OpenAPI Schema generation with &#x60;response_model&#x60;.  Responsible for sanitizing data &amp; converting JSON to &amp; from MongoDBModel.  Contains supplemental function, related to MongoDBModel, mostly proxied to corresponding functions inside model (ex. save, update)  Heavily uses &#x60;Meta&#x60; class for fine-tuning input &amp; output. Main fields are:     * exclude - set of fields that are excluded when serializing to dict                 and sanitizing list of dicts     * model - class of the MongoDBModel to use, inherits fields from it     * write_only_fields - set of fields that can be accepted in request,                           but excluded when serializing to dict     * read_only_fields - set of fields that cannot be accepted in request,                           but included when serializing to dict  Example usage:  .. code-block:: python      app &#x3D; FastAPI()       class SomeModel(MongoDBModel):         field1: str       @openapi.patch     class SomeSerializer(Serializer):         read_only1: str &#x3D; \&quot;const\&quot;         write_only2: int         not_visible: str &#x3D; \&quot;42\&quot;          class Meta:             model &#x3D; SomeModel             exclude &#x3D; {\&quot;not_visible\&quot;}             write_only_fields &#x3D; {\&quot;write_only2\&quot;}             read_only_fields &#x3D; {\&quot;read_only1\&quot;}       @app.get(\&quot;/\&quot;, response_model&#x3D;SomeSerializer.response_model)     async def root(serializer: SomeSerializer):         model_instance &#x3D; await serializer.save()         return model_instance.dict()  POST-ing to this route following JSON:  .. code-block:: json      {\&quot;read_only1\&quot;: \&quot;a\&quot;, \&quot;write_only2\&quot;: 123, \&quot;field1\&quot;: \&quot;b\&quot;}  Should return following response:  .. code-block:: json      {\&quot;id\&quot;: 1, \&quot;field1\&quot;: \&quot;b\&quot;, \&quot;read_only1\&quot;: \&quot;const\&quot;} | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**image** | str,  | str,  |  | 
**name** | str,  | str,  |  | 
**description** | str,  | str,  |  | 
**active** | bool,  | BoolClass,  |  | [optional] if omitted the server will use the default value of True
**created** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] 
**default** | bool,  | BoolClass,  |  | [optional] if omitted the server will use the default value of False
**metadata** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | [optional] if omitted the server will use the default value of {}
**[properties](#properties)** | list, tuple,  | tuple,  |  | [optional] 
**[status](#status)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | [optional] if omitted the server will use the default value of draft
**updated** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# properties

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

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

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | if omitted the server will use the default value of draft

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AssetStatus](AssetStatus.md) | [**AssetStatus**](AssetStatus.md) | [**AssetStatus**](AssetStatus.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

