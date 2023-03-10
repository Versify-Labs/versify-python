# coding: utf-8

"""
    Versify API

    Versify API  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""

from versify.paths.v2_users_me.get import GetCurrentUserV2UsersMeGet
from versify.paths.v2_users_me.put import UpdateCurrentUserV2UsersMePut


class UsersApi(
    GetCurrentUserV2UsersMeGet,
    UpdateCurrentUserV2UsersMePut,
):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """
    pass
