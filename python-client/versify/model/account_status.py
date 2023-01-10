# coding: utf-8

"""
    Versify API

    Versify API documentation  # noqa: E501

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


class AccountStatus(
    schemas.EnumBase,
    schemas.StrSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    An enumeration.
    """


    class MetaOapg:
        enum_value_to_name = {
            "active": "ACTIVE",
            "inactive": "INACTIVE",
        }
    
    @schemas.classproperty
    def ACTIVE(cls):
        return cls("active")
    
    @schemas.classproperty
    def INACTIVE(cls):
        return cls("inactive")
