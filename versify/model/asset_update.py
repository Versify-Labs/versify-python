# coding: utf-8

"""
    Versify API

    Versify API  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from versify import schemas  # noqa: F401


class AssetUpdate(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Base Serializer class.

Almost ALWAYS should be used in conjunction with
`fastapi_contrib.serializers.openapi.patch` decorator to correctly handle
inherited model fields and OpenAPI Schema generation with `response_model`.

Responsible for sanitizing data & converting JSON to & from MongoDBModel.

Contains supplemental function, related to MongoDBModel,
mostly proxied to corresponding functions inside model (ex. save, update)

Heavily uses `Meta` class for fine-tuning input & output. Main fields are:
    * exclude - set of fields that are excluded when serializing to dict
                and sanitizing list of dicts
    * model - class of the MongoDBModel to use, inherits fields from it
    * write_only_fields - set of fields that can be accepted in request,
                          but excluded when serializing to dict
    * read_only_fields - set of fields that cannot be accepted in request,
                          but included when serializing to dict

Example usage:

.. code-block:: python

    app = FastAPI()


    class SomeModel(MongoDBModel):
        field1: str


    @openapi.patch
    class SomeSerializer(Serializer):
        read_only1: str = "const"
        write_only2: int
        not_visible: str = "42"

        class Meta:
            model = SomeModel
            exclude = {"not_visible"}
            write_only_fields = {"write_only2"}
            read_only_fields = {"read_only1"}


    @app.get("/", response_model=SomeSerializer.response_model)
    async def root(serializer: SomeSerializer):
        model_instance = await serializer.save()
        return model_instance.dict()

POST-ing to this route following JSON:

.. code-block:: json

    {"read_only1": "a", "write_only2": 123, "field1": "b"}

Should return following response:

.. code-block:: json

    {"id": 1, "field1": "b", "read_only1": "const"}
    """


    class MetaOapg:
        required = {
            "image",
            "name",
            "description",
        }
        
        class properties:
            description = schemas.StrSchema
            
            
            class image(
                schemas.StrSchema
            ):
            
            
                class MetaOapg:
                    format = 'uri'
                    max_length = 2083
                    min_length = 1
            name = schemas.StrSchema
            active = schemas.BoolSchema
            created = schemas.IntSchema
            default = schemas.BoolSchema
            metadata = schemas.AnyTypeSchema
            
            
            class properties(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    items = schemas.DictSchema
            
                def __new__(
                    cls,
                    _arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]], typing.List[typing.Union[MetaOapg.items, dict, frozendict.frozendict, ]]],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'properties':
                    return super().__new__(
                        cls,
                        _arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> MetaOapg.items:
                    return super().__getitem__(i)
            
            
            class status(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
                    @classmethod
                    @functools.lru_cache()
                    def all_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            AssetStatus,
                        ]
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'status':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            updated = schemas.IntSchema
            __annotations__ = {
                "description": description,
                "image": image,
                "name": name,
                "active": active,
                "created": created,
                "default": default,
                "metadata": metadata,
                "properties": properties,
                "status": status,
                "updated": updated,
            }
    
    image: MetaOapg.properties.image
    name: MetaOapg.properties.name
    description: MetaOapg.properties.description
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["image"]) -> MetaOapg.properties.image: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["active"]) -> MetaOapg.properties.active: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created"]) -> MetaOapg.properties.created: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["default"]) -> MetaOapg.properties.default: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["properties"]) -> MetaOapg.properties.properties: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated"]) -> MetaOapg.properties.updated: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["description", "image", "name", "active", "created", "default", "metadata", "properties", "status", "updated", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["image"]) -> MetaOapg.properties.image: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["active"]) -> typing.Union[MetaOapg.properties.active, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created"]) -> typing.Union[MetaOapg.properties.created, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["default"]) -> typing.Union[MetaOapg.properties.default, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["properties"]) -> typing.Union[MetaOapg.properties.properties, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated"]) -> typing.Union[MetaOapg.properties.updated, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["description", "image", "name", "active", "created", "default", "metadata", "properties", "status", "updated", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        image: typing.Union[MetaOapg.properties.image, str, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        description: typing.Union[MetaOapg.properties.description, str, ],
        active: typing.Union[MetaOapg.properties.active, bool, schemas.Unset] = schemas.unset,
        created: typing.Union[MetaOapg.properties.created, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        default: typing.Union[MetaOapg.properties.default, bool, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        properties: typing.Union[MetaOapg.properties.properties, list, tuple, schemas.Unset] = schemas.unset,
        status: typing.Union[MetaOapg.properties.status, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        updated: typing.Union[MetaOapg.properties.updated, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'AssetUpdate':
        return super().__new__(
            cls,
            *_args,
            image=image,
            name=name,
            description=description,
            active=active,
            created=created,
            default=default,
            metadata=metadata,
            properties=properties,
            status=status,
            updated=updated,
            _configuration=_configuration,
            **kwargs,
        )

from versify.model.asset_status import AssetStatus
