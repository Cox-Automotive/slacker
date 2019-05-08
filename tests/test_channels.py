#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import unittest

from mock import patch, Mock
from . import stubs

from slackest import Channels


class TestUtils(unittest.TestCase):
    @patch('slackest.base_api.requests')
    def test_get_channel_id(self, mock_requests):
        json_to_text = json.dumps(stubs.good_channel_list_response)

        mock_requests.get.return_value = Mock(
            status_code=200, text=json_to_text,
        )

        channels = Channels(token='aaa')

        self.assertEqual(
            'C0G9QF9GW', channels.get_channel_id('random')
        )

    @patch('slackest.base_api.requests')
    def test_get_channel_id_without_channel(self, mock_requests):
        json_to_text = json.dumps(stubs.good_channel_list_response)

        mock_requests.get.return_value = Mock(
            status_code=200, text=json_to_text,
        )

        channels = Channels(token='aaa')

        self.assertEqual(
            None, channels.get_channel_id('fake_group')
        )
