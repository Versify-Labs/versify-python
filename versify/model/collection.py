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


class Collection(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    A collection document in the database.
    """


    class MetaOapg:
        required = {
            "name",
            "account",
        }
        
        class properties:
            account = schemas.StrSchema
            name = schemas.StrSchema
            _id = schemas.StrSchema
            contract_address = schemas.StrSchema
            created = schemas.IntSchema
            default = schemas.BoolSchema
            description = schemas.StrSchema
            image = schemas.StrSchema
            metadata = schemas.DictSchema
            object = schemas.StrSchema
            signature = schemas.StrSchema
            status = schemas.StrSchema
            transaction = schemas.StrSchema
            updated = schemas.IntSchema
            uri = schemas.StrSchema
            __annotations__ = {
                "account": account,
                "name": name,
                "_id": _id,
                "contract_address": contract_address,
                "created": created,
                "default": default,
                "description": description,
                "image": image,
                "metadata": metadata,
                "object": object,
                "signature": signature,
                "status": status,
                "transaction": transaction,
                "updated": updated,
                "uri": uri,
            }
    
    name: MetaOapg.properties.name
    account: MetaOapg.properties.account
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["account"]) -> MetaOapg.properties.account: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["_id"]) -> MetaOapg.properties._id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["contract_address"]) -> MetaOapg.properties.contract_address: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created"]) -> MetaOapg.properties.created: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["default"]) -> MetaOapg.properties.default: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["image"]) -> MetaOapg.properties.image: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["object"]) -> MetaOapg.properties.object: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["signature"]) -> MetaOapg.properties.signature: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["transaction"]) -> MetaOapg.properties.transaction: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updated"]) -> MetaOapg.properties.updated: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["uri"]) -> MetaOapg.properties.uri: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["account", "name", "_id", "contract_address", "created", "default", "description", "image", "metadata", "object", "signature", "status", "transaction", "updated", "uri", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["account"]) -> MetaOapg.properties.account: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["_id"]) -> typing.Union[MetaOapg.properties._id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["contract_address"]) -> typing.Union[MetaOapg.properties.contract_address, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created"]) -> typing.Union[MetaOapg.properties.created, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["default"]) -> typing.Union[MetaOapg.properties.default, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["image"]) -> typing.Union[MetaOapg.properties.image, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["object"]) -> typing.Union[MetaOapg.properties.object, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["signature"]) -> typing.Union[MetaOapg.properties.signature, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> typing.Union[MetaOapg.properties.status, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["transaction"]) -> typing.Union[MetaOapg.properties.transaction, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updated"]) -> typing.Union[MetaOapg.properties.updated, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["uri"]) -> typing.Union[MetaOapg.properties.uri, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["account", "name", "_id", "contract_address", "created", "default", "description", "image", "metadata", "object", "signature", "status", "transaction", "updated", "uri", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        account: typing.Union[MetaOapg.properties.account, str, ],
        _id: typing.Union[MetaOapg.properties._id, str, schemas.Unset] = schemas.unset,
        contract_address: typing.Union[MetaOapg.properties.contract_address, str, schemas.Unset] = schemas.unset,
        created: typing.Union[MetaOapg.properties.created, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        default: typing.Union[MetaOapg.properties.default, bool, schemas.Unset] = schemas.unset,
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        image: typing.Union[MetaOapg.properties.image, str, schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        object: typing.Union[MetaOapg.properties.object, str, schemas.Unset] = schemas.unset,
        signature: typing.Union[MetaOapg.properties.signature, str, schemas.Unset] = schemas.unset,
        status: typing.Union[MetaOapg.properties.status, str, schemas.Unset] = schemas.unset,
        transaction: typing.Union[MetaOapg.properties.transaction, str, schemas.Unset] = schemas.unset,
        updated: typing.Union[MetaOapg.properties.updated, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        uri: typing.Union[MetaOapg.properties.uri, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'Collection':
        return super().__new__(
            cls,
            *_args,
            name=name,
            account=account,
            _id=_id,
            contract_address=contract_address,
            created=created,
            default=default,
            description=description,
            image=image,
            metadata=metadata,
            object=object,
            signature=signature,
            status=status,
            transaction=transaction,
            updated=updated,
            uri=uri,
            _configuration=_configuration,
            **kwargs,
        )