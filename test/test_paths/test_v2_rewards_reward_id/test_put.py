# coding: utf-8

"""


    Generated by: https://openapi-generator.tech
"""

import unittest
from unittest.mock import patch

import urllib3

import versify
from versify.paths.v2_rewards_reward_id import put  # noqa: E501
from versify import configuration, schemas, api_client

from .. import ApiTestMixin


class TestV2RewardsRewardId(ApiTestMixin, unittest.TestCase):
    """
    V2RewardsRewardId unit test stubs
        Update reward  # noqa: E501
    """
    _configuration = configuration.Configuration()

    def setUp(self):
        used_api_client = api_client.ApiClient(configuration=self._configuration)
        self.api = put.ApiForput(api_client=used_api_client)  # noqa: E501

    def tearDown(self):
        pass

    response_status = 200






if __name__ == '__main__':
    unittest.main()
