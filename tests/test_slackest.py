#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import unittest

from mock import patch, Mock
from . import stubs

from slackest import Slackest


class TestUtils(unittest.TestCase):
    # create_channel
    @patch('slackest.requests')
    def test_create_channel(self, mock_requests):
        json_to_text = json.dumps(stubs.good_channel_info_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        new_channel_id = sc.create_channel('busting', False, ["U0G9QF9C6", "U1QNSQB9U"]).body['channel'].get('id')
        self.assertEqual('C1H9RESGL', new_channel_id)

    @patch('slackest.requests')
    def test_create_channel_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_channel_info_response)
        mock_requests.post.return_value = Mock(
            status_code=404, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.create_channel('busting', False, ["U0G9QF9C6", "U1QNSQB9U"]).body['error']
        self.assertEqual('channel_not_found', error)

    # get_channels
    @patch('slackest.requests')
    def test_get_channels(self, mock_requests):
        json_to_text = json.dumps(stubs.good_conversation_list_response)
        mock_requests.get.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        channel_id = sc.get_channels(False, 500, ['public_channel','private_channel','mpim','im']).body['channels'][0].get('id')
        self.assertEqual('G0AKFJBEU', channel_id)

    @patch('slackest.requests')
    def test_get_channels_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_conversation_list_response)
        mock_requests.get.return_value = Mock(
            status_code=404, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.get_channels(False, 500, ['public_channel','private_channel','mpim','im']).body['error']
        self.assertEqual('invalid_auth', error)

    # list_all_users
    @patch('slackest.requests')
    def test_list_all_users(self, mock_requests):
        json_to_text = json.dumps(stubs.good_user_list_response)
        mock_requests.get.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        all_users = sc.list_all_users().body['members']
        first_user_id = all_users[0].get('id')
        self.assertEqual('W012A3CDE', first_user_id)

    @patch('slackest.requests')
    def test_list_all_users_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_user_list_response)
        mock_requests.get.return_value = Mock(
            status_code=500, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.list_all_users().body['error']
        self.assertEqual('fatal_error', error)

    # kick_user
    @patch('slackest.requests')
    def test_kick_user(self, mock_requests):
        json_to_text = json.dumps(stubs.good_kick_user_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        ku = sc.kick_user('C0G9QF9GW', 'U0G9QF9C6').body['ok']
        self.assertEqual('true', ku)

    @patch('slackest.requests')
    def test_kick_user_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_kick_user_response)
        mock_requests.post.return_value = Mock(
            status_code=500, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.kick_user('C0G9QF9GW', 'U0G9QF9C6').body['error']
        self.assertEqual('user_not_found', error)

    # history_all
    @patch('slackest.requests')
    def test_get_conversation_history(self, mock_requests):
        json_to_text = json.dumps(stubs.good_conversation_history_response)
        mock_requests.get.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        second_user = sc.history_all('asd', 500).body['messages'][1].get('user')
        self.assertEqual('U061F7AUR', second_user)

    @patch('slackest.requests')
    def test_get_conversation_history_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_conversation_history_response)
        mock_requests.get.return_value = Mock(
            status_code=404, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.history_all('NOTFOUND', 500).body['error']
        self.assertEqual('channel_not_found', error)

    # post_message_to_channel
    @patch('slackest.requests')
    def test_post_message_to_channel(self, mock_requests):
        json_to_text = json.dumps(stubs.good_conversation_history_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        message_user = sc.post_message_to_channel('slimer', "Here's a message for you").body['messages'][0].get('user')
        self.assertEqual('U012AB3CDE', message_user)

    @patch('slackest.requests')
    def test_post_message_to_channel_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_conversation_history_response)
        mock_requests.post.return_value = Mock(
            status_code=500, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.post_message_to_channel('slimer', "Here's a message for you").body['error']
        self.assertEqual('channel_not_found', error)

    # post_thread_to_message
    @patch('slackest.requests')
    def test_post_thread_to_message(self, mock_requests):
        json_to_text = json.dumps(stubs.good_post_thread_to_message_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        username = sc.post_thread_to_message('slimer', "Here's a message for you", '1503435956.000247').body['message'].get('username')
        self.assertEqual('ecto1', username)

    @patch('slackest.requests')
    def test_post_thread_to_message_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_post_thread_to_message_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.post_thread_to_message('slimer', "Here's a message for you", '1503435956.000247').body['error']
        self.assertEqual('is_archived', error)

    # add_member_to_channel
    @patch('slackest.requests')
    def test_add_member_to_channel(self, mock_requests):
        json_to_text = json.dumps(stubs.good_add_member_to_channel_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        name = sc.add_member_to_channel('C012AB3CD', 'U2345678901').body['channel'].get('name')
        self.assertEqual('general', name)

    @patch('slackest.requests')
    def test_add_member_to_channel_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_add_member_to_channel_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.add_member_to_channel('C012AB3CD', 'U2345678901').body['error']
        self.assertEqual('method_not_supported_for_channel_type', error)

    # get_channel_info
    @patch('slackest.requests')
    def test_get_channel_info(self, mock_requests):
        json_to_text = json.dumps(stubs.good_channel_info_response)
        mock_requests.get.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        channel_name = sc.get_channel_info('C0G9QF9GW').body['channel'].get('name')
        self.assertEqual('busting', channel_name)

    @patch('slackest.requests')
    def test_get_channel_info_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_channel_info_response)
        mock_requests.get.return_value = Mock(
            status_code=404, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.get_channel_info('NOTFOUND').body['error']
        self.assertEqual('channel_not_found', error)

    # get_replies
    @patch('slackest.requests')
    def test_get_replies(self, mock_requests):
        json_to_text = json.dumps(stubs.good_get_replies_response)
        mock_requests.get.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        replies = sc.get_replies('C0G9QF9GW', '1482960137.003543').body['messages'][0].get['reply_count']
        self.assertEqual(3, replies)

    @patch('slackest.requests')
    def test_get_replies(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_get_replies_response)
        mock_requests.get.return_value = Mock(
            status_code=404, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.get_replies('C0G9QF9GW', '1482960137.003543').body['error']
        self.assertEqual('thread_not_found', error)

    # set_purpose
    @patch('slackest.requests')
    def test_set_purpose(self, mock_requests):
        json_to_text = json.dumps(stubs.good_set_purpose_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        purpose = sc.set_purpose('C0G9QF9GW', 'My purpose').body['purpose']
        self.assertEqual('My purpose', purpose)

    @patch('slackest.requests')
    def test_set_purpose_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_set_purpose_response)
        mock_requests.post.return_value = Mock(
            status_code=500, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.set_purpose('C0G9QF9GW', 'My purpose is entirely too long').body['error']
        self.assertEqual('too_long', error)

    # set_topic
    @patch('slackest.requests')
    def test_set_topic(self, mock_requests):
        json_to_text = json.dumps(stubs.good_set_topic_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        topic = sc.set_topic('C0G9QF9GW', 'My topic').body['topic']
        self.assertEqual('My topic', topic)

    @patch('slackest.requests')
    def test_set_topic_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_set_topic_response)
        mock_requests.post.return_value = Mock(
            status_code=500, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.set_topic('C0G9QF9GW', 'My topic').body['error']
        self.assertEqual('user_is_restricted', error)

    # upload_file
    @patch('slackest.requests')
    def test_upload_file(self, mock_requests):
        json_to_text = json.dumps(stubs.good_upload_file_response)
        mock_requests.post.return_value = Mock(
            status_code=200, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        upload = sc.upload_file('README.rst', 'C0G9QF9GW').body['file'].get('id')
        self.assertEqual('F0TD00400', upload)

    @patch('slackest.requests')
    def test_upload_file_error(self, mock_requests):
        json_to_text = json.dumps(stubs.bad_upload_file_response)
        mock_requests.post.return_value = Mock(
            status_code=404, text=json_to_text,
        )
        sc = Slackest(token='aaa')
        error = sc.upload_file('README.rst', 'C0G9QF9GW').body['error']
        self.assertEqual('invalid_auth', error)
