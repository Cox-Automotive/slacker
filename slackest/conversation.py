import datetime
import time

from .base_api import BaseAPI
from .constants import *
from .slackest_error import SlackestError

class Conversation(BaseAPI):
    """Follows the Slack Conversation API.
    See https://api.slack.com/docs/conversations-api#methods"""

    # A Python 2 and Python 3 compatible timestamp
    now = datetime.datetime.now().timetuple()
    timestamp = float((time.mktime(now)+datetime.datetime.now().microsecond/1000000.0))

    def archive(self, channel):
        """
        Archives a channel

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversation.archive', data={'channel': channel})

    def close(self, channel):
        """
        Closes a channel

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.close', data={'channel': channel})

    def create(self, name, is_private=True, users=[]):
        """
        Creates a channel

        :param name: The channel name
        :type name: str
        :param is_private: Determines if channel is private (like a group)
        :type is_private: bool
        :param users: A list of User IDs to add to the channel
        :type users: list[str]
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        return self.post('conversations.create',
                         data={'name': name, 'is_private': str(is_private).lower(),
                               'user_ids': users})

    def history(self, channel, cursor=None, inclusive=False, limit=100,
                latest=timestamp, oldest=0):
        """
        Fetches history of messages and events from a channel

        :param channel: The channel ID
        :type channel: str
        :param cursor: the cursor id of the next set of history
        :type cursor: str
        :param inclusive: Include messages with latest or oldest timestamp in results
        :type inclusive: bool
        :param limit: The number of messages to return
        :type limit: int
        :param latest: End of time range to include in results
        :type latest: str
        :param oldest: Start of time range to include in results
        :type oldest: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('conversations.history',
                        data={'channel': channel, 'cursor': cursor,
                              'inclusive': int(inclusive), 'limit': limit,
                              'latest': latest, 'oldest': oldest})

    def history_all(self, channel):
        """
        Fetches all history of messages and events from a channel

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        response = self.get('conversations.history', params={'channel': channel})
        conversations = response.body.get('messages', [])
        next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
        while next_cursor:
            response = self.get('conversations.history',
                                params={'channel':channel, 'cursor': next_cursor})
            if response is not None:
                conversations.extend(response.body.get('messages', []))
                next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
                time.sleep(DEFAULT_API_SLEEP)
            else:
                raise SlackestError("Null response received. You've probably hit the rate limit.")

        if conversations:
            response.body['messages'] = conversations
        yield response

    def info(self, channel, include_locale=False, include_num_members=False):
        """
        Gets information about a channel.

        :param channel: The channel ID
        :type channel: str
        :param include_locale: Include the locale of the members in the channel
        :type include_locale: bool
        :param include_num_members: Include the number of members in the channel
        :type include_num_members: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.info', data={
            'channel': channel,
            'include_locale': str(include_locale).lower(),
            'include_num_members': str(include_num_members).lower()})

    def invite(self, channel, users=[]):
        """
        Invites users to a channel

        :param name: The channel ID
        :type name: str
        :param users: A list of User IDs to invite to the channel
        :type users: list[str]
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(users, (tuple, list)):
            users = ','.join(users)
        return self.post('conversations.invite', data={'channel': channel, 'users': users})

    def join(self, channel):
        """
        Allows a user object to join a channel

        :param name: The channel ID
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.join', data={'channel': channel})

    def kick(self, channel, user):
        """
        Removes a user from a channel

        :param channel: The channel ID
        :type channel: str
        :param user: The user ID
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.kick', data={'channel': channel, 'user': user})

    def leave(self, channel):
        """
        Allows a user object to leave a channel

        :param name: The channel ID
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.leave', data={'channel': channel})

    def list(self, cursor=None, exclude_archived=False, limit=100, types="public_channel"):
        """
        Lists channels

        :param cursor: the cursor id of the next set of the list
        :type cursor: str
        :param exclude_archived: Exclude archived channels
        :type exclude_archived: bool
        :param limit: The number of conversations to return
        :type limit: int
        :param types: The type of channel to return, can be one of public_channel, private_channel
        :type types: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        yield self.post('conversations.list',
                         data={'cursor': cursor, 'exclude_archived': str(exclude_archived).lower(),
                               'limit': limit, 'types': types})

    def list_all(self, exclude_archived=False, types="public_channel"):
        """
        Lists all channels

        :param exclude_archived: Exclude archived channels
        :type exclude_archived: bool
        :param types: The type of channel to return, can be one of public_channel, private_channel
        :type types: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        response = self.get('conversations.list',
                            params={'exclude_archived': str(exclude_archived).lower(),
                                    'types': types})
        channels = response.body.get('channels', [])
        next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
        while next_cursor:
            response = self.get('conversations.list',
                                params={'exclude_archived': str(exclude_archived).lower(),
                                        'types': types, 'cursor': next_cursor})
            if response is not None:
                channels.extend(response.body.get('channels', []))
                next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
                time.sleep(DEFAULT_API_SLEEP)
            else:
                raise SlackestError("Null response received. You've probably hit the rate limit.")

        if channels:
            response.body['channels'] = channels
        return response

    def members(self, channel, cursor=None, limit=100):
        """
        Lists members of a channel

        :param channel: The channel ID
        :type channel: str
        :param cursor: the cursor id of the next set of the list
        :type cursor: str
        :param limit: The number of messages to return
        :type limit: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.members',
                         data={'channel': channel, 'cursor': cursor, 'limit': limit})

    def members_all(self, channel):
        """
        Lists all members of a channel

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        response = self.get('conversations.members', params={'channel': channel})
        members = response.body.get('members', [])
        next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
        while next_cursor:
            response = self.get('conversations.members',
                                params={'channel': channel, 'cursor': next_cursor})
            if response is not None:
                members.extend(response.body.get('members', []))
                next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
                time.sleep(DEFAULT_API_SLEEP)
            else:
                raise SlackestError("Null response received. You've probably hit the rate limit.")

        if members:
            response.body['members'] = members
        yield response

    def open(self, channel, return_im=True, users=[]):
        """
        Opens or resumes DMs or multi person DMs

        :param channel: The channel ID
        :type channel: str
        :param return_im: Indicates you wnat the full IM channel definition in the response
        :type return_im: bool
        :param user_ids: A list of User IDs to invite to the channel
        :type user_ids: list[str]
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        self.post('conversations.open',
                  data={'channel': channel, 'return_im': str(return_im).lower(), 'users': users})

    def rename(self, channel, name):
        """
        Renames a channel

        :param channel: The channel ID to rename
        :type channel: str
        :param name: The new name of the channel
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        self.post('conversations.rename', data={'channel': channel, 'name': name})

    def replies(self, channel, time_stamp, cursor=None, inclusive=False, limit=100,
                latest=timestamp, oldest=0):
        """
        Fetches replies in a thread of messages

        :param channel: The channel ID
        :type channel: str
        :param time_stamp: Unique identifier of a thread's parent message
        :type time_stamp: str
        :param cursor: the cursor id of the next set of replies
        :type cursor: str
        :param inclusive: Include messages with latest or oldest timestamp in results
        :type inclusive: bool
        :param limit: The number of messages to return
        :type limit: int
        :param latest: End of time range to include in results
        :type latest: str
        :param latest: Start of time range to include in results
        :type oldest: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.replies',
                         data={'channel': channel, 'ts': time_stamp, 'cursor': cursor,
                               'inclusive': int(inclusive), 'limit': limit,
                               'latest': latest, 'oldest': oldest})

    def replies_all(self, channel, time_stamp):
        """
        Fetches all replies in a thread of messages

        :param channel: The channel ID
        :type channel: str
        :param time_stamp: Unique identifier of a thread's parent message
        :type time_stamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        response = self.get('conversations.replies',
                            params={'channel': channel, 'ts': time_stamp})
        replies = response.body.get('message', [])
        next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
        while next_cursor:
            response = self.get('conversations.replies',
                                params={'channel': channel, 'ts': time_stamp,
                                        'cursor': next_cursor})
            if response is not None:
                replies.extend(response.body.get('message', []))
                next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
                time.sleep(DEFAULT_API_SLEEP)
            else:
                raise SlackestError("Null response received. You've probably hit the rate limit.")

        if replies:
            response.body['message'] = replies
        yield response

    def setPurpose(self, channel, purpose):
        """
        Assigns purpose to a channel

        :param channel: The channel ID
        :type channel: str
        :param purpose: The new purpose of the channel
        :type purpose: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.setPurpose', data={'channel': channel, 'purpose': purpose})

    def setTopic(self, channel, topic):
        """
        Assigns topic to a channel

        :param channel: The channel ID
        :type channel: str
        :param topic: The new topic of the channel
        :type topic: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.setTopic', data={'channel': channel, 'topic': topic})

    def unarchive(self, channel):
        """
        Unarchives a channel

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('conversations.unarchive', data={'channel': channel})
