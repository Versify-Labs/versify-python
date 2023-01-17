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


class TriggerScheduleConfig(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    A trigger schedule configuration.
    """


    class MetaOapg:
        
        class properties:
            at = schemas.IntSchema
            cron = schemas.StrSchema
            end = schemas.IntSchema
            rate = schemas.StrSchema
            start = schemas.IntSchema
            __annotations__ = {
                "at": at,
                "cron": cron,
                "end": end,
                "rate": rate,
                "start": start,
            }
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["at"]) -> MetaOapg.properties.at: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["cron"]) -> MetaOapg.properties.cron: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["end"]) -> MetaOapg.properties.end: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["rate"]) -> MetaOapg.properties.rate: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["start"]) -> MetaOapg.properties.start: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["at", "cron", "end", "rate", "start", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["at"]) -> typing.Union[MetaOapg.properties.at, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["cron"]) -> typing.Union[MetaOapg.properties.cron, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["end"]) -> typing.Union[MetaOapg.properties.end, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["rate"]) -> typing.Union[MetaOapg.properties.rate, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["start"]) -> typing.Union[MetaOapg.properties.start, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["at", "cron", "end", "rate", "start", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        at: typing.Union[MetaOapg.properties.at, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        cron: typing.Union[MetaOapg.properties.cron, str, schemas.Unset] = schemas.unset,
        end: typing.Union[MetaOapg.properties.end, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        rate: typing.Union[MetaOapg.properties.rate, str, schemas.Unset] = schemas.unset,
        start: typing.Union[MetaOapg.properties.start, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TriggerScheduleConfig':
        return super().__new__(
            cls,
            *_args,
            at=at,
            cron=cron,
            end=end,
            rate=rate,
            start=start,
            _configuration=_configuration,
            **kwargs,
        )
