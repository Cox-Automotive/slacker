# Copyright 2019 Cox Automotive, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import json
import requests
import time

from slackest.utils import get_item_id_by_name


API_BASE_URL = 'https://slack.com/api/{api}'
DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 0
# seconds to wait after a 429 error if Slack's API doesn't provide one
DEFAULT_WAIT = 20
DEFAULT_API_SLEEP = 5

__version__ = '0.13.2'
__all__ = ['Error', 'Response', 'BaseAPI', 'API', 'Auth', 'Users', 'Groups',
           'Conversation', 'Channels', 'Chat', 'IM', 'IncomingWebhook',
           'Search', 'Files', 'Stars', 'Emoji', 'Presence', 'RTM', 'Team',
           'Reactions', 'Pins', 'UserGroups', 'UserGroupsUsers', 'MPIM',
           'OAuth', 'DND', 'Bots', 'FilesComments', 'Reminders', 'TeamProfile',
           'UsersProfile', 'IDPGroups', 'Apps', 'AppsPermissions', 'Slackest',
           'Dialog']


class SlackestError(Exception):
    pass


class Response(object):
    def __init__(self, body):
        self.raw = body
        self.body = json.loads(body)
        self.successful = self.body['ok']
        self.error = self.body.get('error')

    def __str__(self):
        return json.dumps(self.body)


class BaseAPI(object):
    def __init__(self, token=None, timeout=DEFAULT_TIMEOUT, proxies=None,
                 session=None, rate_limit_retries=DEFAULT_RETRIES):
        self.token = token
        self.timeout = timeout
        self.proxies = proxies
        self.session = session
        self.rate_limit_retries = rate_limit_retries
        self.retry_max = 10
        self.retry_counter = 0
        self.retry_wait_secs = 1

    def _request(self, method, api, **kwargs):
        """
        Internal request call, with rate limiting retries

        :param method: The method to call: GET, POST, etc.
        :type method: :class:`Request <Request>` object
        :param api: The API endpoint
        :type api: str
        :param kwargs: Various keyword arguments that could be passed to the request
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if self.token:
            kwargs.setdefault('params', {})['token'] = self.token

        # while we have rate limit retries left, fetch the resource and back
        # off as Slack's HTTP response suggests
        for retry_num in range(self.rate_limit_retries):
            response = method(API_BASE_URL.format(api=api),
                              timeout=self.timeout,
                              proxies=self.proxies,
                              **kwargs)

            if response.status_code == requests.codes.ok:
                break

            # handle HTTP 429 as documented at
            # https://api.slack.com/docs/rate-limits
            elif response.status_code == requests.codes.too_many: # HTTP 429
                time.sleep(int(response.headers.get('retry-after', DEFAULT_WAIT)))
                continue

            else:
                response.raise_for_status()

        else:
            # with no retries left, make one final attempt to fetch the resource,
            # but do not handle too_many status differently
            response = method(API_BASE_URL.format(api=api),
                              timeout=self.timeout,
                              proxies=self.proxies,
                              **kwargs)
            response.raise_for_status()

        response = Response(response.text)
        if not response.successful:
            raise SlackestError(response.error)

        return response

    def _session_get(self, url, params=None, **kwargs):
        """
        Internal request GET call with session

        :param url: The URL to request
        :type url: str
        :param params: Dictionary containing URL request parameters (headers, etc.)
        :type params: dict
        :param kwargs: Various keyword arguments that could be passed to the GET
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        kwargs.setdefault('allow_redirects', True)
        return self.session.request(
            method='get', url=url, params=params, **kwargs
        )

    def _session_post(self, url, data=None, **kwargs):
        """
        Internal request POST call with session

        :param url: The URL to request
        :type url: str
        :param params: Dictionary containing request data
        :type params: dict
        :param kwargs: Various keyword arguments that could be passed to the POST
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.session.request(
            method='post', url=url, data=data, **kwargs
        )

    def get(self, api, **kwargs):
        """
        External request GET call, wraps around internal _request.get

        :param api: The API endpoint to connect to
        :type api: str
        :param kwargs: Various keyword arguments that could be passed to the GET
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        try:
            return self._request(
                self._session_get if self.session else requests.get,
                api, **kwargs
            )
        except requests.HTTPError as e:
            # Put a retry here with a short circuit
            if self.retry_counter < self.retry_max:
                self.retry_counter =+ 1
                time.sleep(self.retry_wait_secs)
                self.get(api, **kwargs)
            else:
                raise


    def post(self, api, **kwargs):
        """
        External request POST call, wraps around internal _request.post

        :param api: The API endpoint to connect to
        :type api: str
        :param kwargs: Various keyword arguments that could be passed to the POST
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self._request(
            self._session_post if self.session else requests.post,
            api, **kwargs
        )


class API(BaseAPI):
    def test(self, error=None, **kwargs):
        """
        Allows access to the Slack API test endpoint

        :param error: The API error
        :type error: str
        :param kwargs: Various keyword arguments that could be passed to the request
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if error:
            kwargs['error'] = error

        return self.get('api.test', params=kwargs)


class Auth(BaseAPI):
    def test(self):
        """
        Allows access to the Slack API test endpoint

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('auth.test')

    def revoke(self, test=True):
        """
        Allows access to the Slack API test endpoint

        :param test: Boolean to run the test
        :type test: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('auth.revoke', data={'test': int(test)})


class Dialog(BaseAPI):
    def open(self, dialog, trigger_id):
        """
        Opens a dialog with a user

        :param dialog: JSON-encoded dialog definition
        :type dialog: json
        :param trigger_id: The trigger to post to the user.
        :type trigger_id: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('dialog.open',
                         data={
                             'dialog': json.dumps(dialog),
                             'trigger_id': trigger_id,
                         })


class UsersProfile(BaseAPI):
    def get(self, user=None, include_labels=False):
        """
        Gets a Slack user's profile

        :param user: User to retrieve profile info for
        :type user: str
        :param include_labels: Include labels for each ID in custom profile fields
        :type include_labels: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return super(UsersProfile, self).get(
            'users.profile.get',
            params={'user': user, 'include_labels': str(include_labels).lower()}
        )

    def set(self, user=None, profile=None, name=None, value=None):
        """
        Gets a Slack user's profile

        :param user: ID of user to change
        :type user: str
        :param profile: Collection of key:value pairs presented as a URL-encoded JSON hash
        :type profile: str
        :param name: Name of a single key to set
        :type name: str
        :param value: Value to set a single key to
        :type value: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('users.profile.set',
                         data={
                             'user': user,
                             'profile': profile,
                             'name': name,
                             'value': value
                         })


class UsersAdmin(BaseAPI):
    def invite(self, email, channels=None, first_name=None,
               last_name=None, resend=True):
        """
        DEPRECATED - Invites a user to channel(s) via email. Looks to be deprecated.

        :param email: Email of the user to invite to a channel(s)
        :type email: str
        :param channels: A CSV of channels for the invite.
        :type channels: str
        :param first_name: First name of the invitee
        :type first_name: str
        :param last_name: Last name of the invitee
        :type last_name: str
        :param resend: Whether or not this invite is a resend
        :type resend: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('users.admin.invite',
                         params={
                             'email': email,
                             'channels': channels,
                             'first_name': first_name,
                             'last_name': last_name,
                             'resend': resend
                         })


class Users(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self._profile = UsersProfile(*args, **kwargs)
        self._admin = UsersAdmin(*args, **kwargs)

    @property
    def profile(self):
        return self._profile

    @property
    def admin(self):
        return self._admin

    def info(self, user, include_locale=False):
        """
        Returns information about the user

        :param user: The Slack user ID of the user to look up
        :type user: str
        :param include_locale: Whether or not to include the user's locale
        :type include_locale: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('users.info', params={'user': user, 'include_locale': str(include_locale).lower()})

    def list(self, cursor=None, include_locale=True, limit=500):
        """
        List all users in a Slack team.

        :param cursor: Cursor pagination
        :type cursor: str
        :param include_locale: Receive the user's locale
        :type include_locale: bool
        :param limit: The maximum number of users to return
        :type limit: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('users.list', 
                params={'include_locale': str(include_locale).lower(), 
                    'limit': limit, 'cursor': cursor})

    def list_all(self, include_locale=True):
        """
        Lists all users in a Slack team

        :param include_locale: Receive the user's locale
        :type include_locale: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        response = self.get('users.list', params={'include_locale': str(include_locale).lower()})
        members = response.body.get('members', [])
        next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
        while next_cursor:
            response = self.get('users.list',
                    params={'include_locale': str(include_locale).lower(), 'cursor': next_cursor})
            if response is not None:
                members.extend(response.body.get('members', []))
                next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
                time.sleep(DEFAULT_API_SLEEP)
            else:
                raise SlackestError("Null response received. You've probably hit the rate limit.")

        if members:
            response.body['members'] = members

        return response

    def identity(self):
        """
        Retrieves the user's identity: name, ID, team

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('users.identity')

    def set_active(self):
        """
        Sets the user object to active. DEPRECATED

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('users.setActive')

    def get_presence(self, user):
        """
        Gets the presence of the Slack user

        :param user: The Slack user ID
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('users.getPresence', params={'user': user})

    def set_presence(self, presence):
        """
        Sets the presence of the current Slack user

        :param presence: The presence level of the user: either `auto` or `away`
        :type presence: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('users.setPresence', data={'presence': presence})

    def get_user_id(self, user_name):
        """
        Gets a user ID according to the user's name

        :param user_name: The user's name
        :type user_name: str
        :return: Returns the user ID
        :rtype: str
        """
        members = self.list_all_users().body['members']
        return get_item_id_by_name(members, user_name)


class Groups(BaseAPI):
    def create(self, name):
        """
        Creates a group with the name

        :param name: The group's name
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.create', data={'name': name})

    def create_child(self, channel):
        """
        Takes an existing private channel and performs the following steps:

        * Renames the existing private channel (from "example" to "example-archived").
        * Archives the existing private channel.
        * Creates a new private channel with the name of the existing private channel.
        * Adds all members of the existing private channel to the new private channel.

        :param channel: Private channel to clone and archive
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.createChild', data={'channel': channel})

    def info(self, channel):
        """
        Returns the private channel's information

        :param channel: The private channel's ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('groups.info', params={'channel': channel})

    def list(self, exclude_archived=True, exclude_members=False):
        """
        Lists the private channels that the user has access to

        :param exclude_archived: Don't include archived private channels in the returned list
        :type exclude_archived: bool
        :param exclude_members: Don't include members in the returned list
        :type exclude_members: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('groups.list',
                        params={'exclude_archived': str(exclude_archived).lower(),
                            'exclude_members': str(exclude_members).lower()})

    def history(self, channel, latest=None, oldest=None, count=None,
                inclusive=True):
        """
        Fetches history of messages and events from a private channel

        :param channel: The private channel ID
        :type channel: str
        :param latest: End of time range to include in results
        :type latest: str
        :param oldest: Start of time range to include in results
        :type oldest: str
        :param count: The number of messages to return
        :type count: int
        :param inclusive: Include messages with latest or oldest timestamp in results
        :type inclusive: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('groups.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'count': count,
                            'inclusive': int(inclusive)
                        })

    def invite(self, channel, user):
        """
        Invites a user to a private channel

        :param channel: The private channel ID
        :type channel: str
        :param user: The user ID
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.invite',
                         data={'channel': channel, 'user': user})

    def kick(self, channel, user):
        """
        Removes a user from a private channel

        :param channel: The private channel ID
        :type channel: str
        :param user: The user ID
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.kick',
                         data={'channel': channel, 'user': user})

    def leave(self, channel):
        """
        Allows a user object to remove themselves from a private channel

        :param channel: The private channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.leave', data={'channel': channel})

    def mark(self, channel, ts):
        """
        Moves the read cursor in a private channel

        :param channel: The private channel ID
        :type channel: str
        :param ts: The timestamp of the most recently seen message
        :type ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.mark', data={'channel': channel, 'ts': ts})

    def rename(self, channel, name):
        """
        Renames a private channel

        :param channel: The private channel ID
        :type channel: str
        :param name: The new user-friendly name of the private channel
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.rename',
                         data={'channel': channel, 'name': name})

    def replies(self, channel, thread_ts):
        """
        Retrieve a thread of messages posted to a private channel

        :param channel: The private channel ID
        :type channel: str
        :param thread_ts: Unique identifier of a thread's parent message
        :type thread_ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('groups.replies',
                        params={'channel': channel, 'thread_ts': thread_ts})

    def archive(self, channel):
        """
        Archives a private channel

        :param channel: The private channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.archive', data={'channel': channel})

    def unarchive(self, channel):
        """
        Unarchives a private channel

        :param channel: The private channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.unarchive', data={'channel': channel})

    def open(self, channel):
        """
        Opens a private channel

        :param channel: The private channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.open', data={'channel': channel})

    def close(self, channel):
        """
        Closes a private channel

        :param channel: The private channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.close', data={'channel': channel})

    def set_purpose(self, channel, purpose):
        """
        Sets the purpose of a private channel

        :param channel: The private channel ID
        :type channel: str
        :param purpose: The purpose
        :type purpose: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.setPurpose',
                         data={'channel': channel, 'purpose': purpose})

    def set_topic(self, channel, topic):
        """
        Sets the topic of a private channel

        :param channel: The private channel ID
        :type channel: str
        :param topic: The topic
        :type topic: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.setTopic',
                         data={'channel': channel, 'topic': topic})


class Channels(BaseAPI):
    def create(self, name):
        """
        Creates a public channel

        :param name: The name
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.create', data={'name': name})

    def info(self, channel):
        """
        Retrieves information about a public channel

        :param name: The channel ID
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('channels.info', params={'channel': channel})

    def list(self, exclude_archived=True, exclude_members=False):
        """
        Lists channels

        :param exclude_archived: Exclude archived channels
        :type exclude_archived: bool
        :param exclude_members: Exclude members from being listed
        :type exclude_members: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('channels.list',
                        params={'exclude_archived': str(exclude_archived).lower(),
                                'exclude_members': str(exclude_members).lower()})

    def history(self, channel, latest=None, oldest=None, count=None,
                inclusive=False, unreads=False):
        """
        Fetches history of messages and events from a channel

        :param channel: The channel ID
        :type channel: str
        :param latest: End of time range to include in results
        :type latest: str
        :param oldest: Start of time range to include in results
        :type oldest: str
        :param count: The number of messages to return
        :type count: int
        :param inclusive: Include messages with latest or oldest timestamp in results
        :type inclusive: bool
        :param unreads: Include `unread_count_display` in the output
        :type unreads: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('channels.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'count': count,
                            'inclusive': int(inclusive),
                            'unreads': int(unreads)
                        })

    def mark(self, channel, ts):
        """
        Moves the read cursor in a public channel

        :param channel: The channel ID
        :type channel: str
        :param ts: The timestamp of the most recently seen message
        :type ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.mark',
                         data={'channel': channel, 'ts': ts})

    def join(self, name):
        """
        Allows a user object to join a channel

        :param name: The channel name (#general)
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.join', data={'name': name})

    def leave(self, channel):
        """
        Allows a user object to leave a channel

        :param name: The channel ID
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.leave', data={'channel': channel})

    def invite(self, channel, user):
        """
        Invites a user to a private channel

        :param channel: The channel ID
        :type channel: str
        :param user: The user ID
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.invite',
                         data={'channel': channel, 'user': user})

    def kick(self, channel, user):
        """
        Removes a user from a channel

        :param channel: The private channel ID
        :type channel: str
        :param user: The user ID
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.kick',
                         data={'channel': channel, 'user': user})

    def rename(self, channel, name):
        """
        Renames a channel

        :param channel: The channel ID
        :type channel: str
        :param name: The new user-friendly name of the channel
        :type name: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.rename',
                         data={'channel': channel, 'name': name})

    def replies(self, channel, thread_ts):
        """
        Retrieve a thread of messages posted to a channel

        :param channel: The channel ID
        :type channel: str
        :param thread_ts: Unique identifier of a thread's parent message
        :type thread_ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('channels.replies',
                        params={'channel': channel, 'thread_ts': thread_ts})

    def archive(self, channel):
        """
        Archives a public channel

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.archive', data={'channel': channel})

    def unarchive(self, channel):
        """
        Unarchives a channel

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.unarchive', data={'channel': channel})

    def set_purpose(self, channel, purpose):
        """
        Sets the purpose of a channel

        :param channel: The channel ID
        :type channel: str
        :param purpose: The purpose
        :type purpose: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.setPurpose',
                         data={'channel': channel, 'purpose': purpose})

    def set_topic(self, channel, topic):
        """
        Sets the topic of a channel

        :param channel: The channel ID
        :type channel: str
        :param topic: The topic
        :type topic: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.setTopic',
                         data={'channel': channel, 'topic': topic})

    def get_channel_id(self, channel_name):
        """
        Gets a channel ID according to the channel's name

        :param channel_name: The channel's name
        :type channel_name: str
        :return: Returns the channel ID
        :rtype: str
        """
        channels = self.list().body['channels']
        return get_item_id_by_name(channels, channel_name)


class Conversation(BaseAPI):
    # https://api.slack.com/docs/conversations-api#methods

    # A Python 2 and Python 3 compatible timestamp
    timestamp = float((time.mktime(datetime.datetime.now().timetuple())+datetime.datetime.now().microsecond/1000000.0))

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
                data={'name': name, 'is_private': str(is_private).lower(), 'user_ids': users})

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
                data={'channel': channel, 'cursor': cursor, 'inclusive': int(inclusive),
                    'limit': limit, 'latest': latest, 'oldest': oldest})

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
                                params={'channel':channel,'cursor': next_cursor})
            if response is not None:
                conversations.extend(response.body.get('messages', []))
                next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
                time.sleep(DEFAULT_API_SLEEP)
            else:
                raise SlackestError("Null response received. You've probably hit the rate limit.")

        if conversations:
            response.body['messages'] = conversations
        return response

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
        return self.post('conversations.invite', data={'channel': channel,'users': users})

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
        return self.post('conversations.list', 
                data={'cursor': cursor, 'exclude_archived': str(exclude_archived).lower(), 'limit': limit, 'types': types})

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
                            params={'exclude_archived': str(exclude_archived).lower(), 'types': types})
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
        return self.post('conversations.members', data={'channel': channel, 'cursor': cursor, 'limit': limit})

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
        return response

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
        self.post('conversations.open', data={'channel': channel, 'return_im': str(return_im).lower(), 'users': users})

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

    def replies(self, channel, ts, cursor=None, inclusive=False, limit=100,
            latest=timestamp, oldest=0):
        """
        Fetches replies in a thread of messages

        :param channel: The channel ID
        :type channel: str
        :param ts: Unique identifier of a thread's parent message
        :type ts: str
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
                data={'channel': channel, 'ts': ts, 'cursor': cursor, 'inclusive': int(inclusive),
                    'limit': limit, 'latest': latest, 'oldest': oldest})

    def replies_all(self, channel, ts):
        """
        Fetches all replies in a thread of messages

        :param channel: The channel ID
        :type channel: str
        :param ts: Unique identifier of a thread's parent message
        :type ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        response = self.get('conversations.replies',
                            params={'channel': channel, 'ts': ts})
        replies = response.body.get('message', [])
        next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
        while next_cursor:
            response = self.get('conversations.replies',
                                params={'channel': channel, 'ts': ts, 'cursor': next_cursor})
            if response is not None:
                replies.extend(response.body.get('message', []))
                next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
                time.sleep(DEFAULT_API_SLEEP)
            else:
                raise SlackestError("Null response received. You've probably hit the rate limit.")

        if replies:
            response.body['message'] = replies
        return response

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


class Chat(BaseAPI):

    def post_message(self, channel, text=None, username=None, as_user=False,
                     parse=None, link_names=None, attachments=None,
                     unfurl_links=None, unfurl_media=None, icon_url=None,
                     icon_emoji=None, thread_ts=None, reply_broadcast=None):
        """
        Posts a message to a channel
        
        :param channel: The channel ID
        :type channel: str
        :param text: Text of the message to post
        :type text: str
        :param username: The username to post as, must be used w/ as_user
        :type username: str
        :param as_user: Posts as the user instead of a bot
        :type as_user: bool
        :param parse: Change how messages are treated
        :type parse: str
        :param link_names: Find and link channel names and username
        :type link_names: str
        :param attachments: JSON based array of structured attachments
        :type attachments: JSON
        :param unfurl_links: Enable unfurling of links
        :type unfurl_links: str
        :param unfurl_media: Enable unfurling of media
        :type unfurl_media: str
        :param icon_url: The icon URL
        :type icon_url: str
        :param icon_emoji: Emoji to use as the icon for this message
        :type icon_emoji: str
        :param thread_ts: Provide another messages ts value to make this message a reply
        :type thread_ts: str
        :param reply_broadcast: Indicates whether reply should be visible in the channel
        :type reply_broadcast: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # Ensure attachments are json encoded
        if attachments:
            if isinstance(attachments, list):
                attachments = json.dumps(attachments)

        return self.post('chat.postMessage',
                         data={
                             'channel': channel,
                             'text': text,
                             'username': username,
                             'as_user': str(as_user).lower(),
                             'parse': parse,
                             'link_names': link_names,
                             'attachments': attachments,
                             'unfurl_links': unfurl_links,
                             'unfurl_media': unfurl_media,
                             'icon_url': icon_url,
                             'icon_emoji': icon_emoji,
                             'thread_ts': thread_ts,
                             'reply_broadcast': reply_broadcast
                         })

    def me_message(self, channel, text):
        """
        Share a me message to a channel  
        
        :param channel: The channel to post to 
        :type channel: str
        :param text: The text of the message
        :type text: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('chat.meMessage',
                         data={'channel': channel, 'text': text})

    def command(self, channel, command, text):
        """
        DEPRECATED? Run a command in a chat
        
        :param channel: The channel ID
        :type channel: str
        :param command: The command to run
        :type command: str
        :param text: The text attached to the command
        :type text: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('chat.command',
                         data={
                             'channel': channel,
                             'command': command,
                             'text': text
                         })

    def update(self, channel, ts, text, attachments=None, parse=None,
               link_names=None, as_user=False):
        """
        Updates a message in a channel
        
        :param channel: The channel ID
        :type channel: str
        :param ts: Timestamp of the message to be updated
        :type ts: str
        :param text: New text for the message
        :type text: str
        :param attachments: JSON array of structured attachments
        :type attachments: JSON
        :param parse: Change hor messages are treated
        :type parse: str
        :param link_names: Find and link channel names
        :type link_names: str
        :param as_user: Update the message as the authed user
        :type as_user: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # Ensure attachments are json encoded
        if attachments is not None and isinstance(attachments, list):
            attachments = json.dumps(attachments)
        return self.post('chat.update',
                         data={
                             'channel': channel,
                             'ts': ts,
                             'text': text,
                             'attachments': attachments,
                             'parse': parse,
                             'link_names': str(link_names).lower(),
                             'as_user': str(as_user).lower,
                         })

    def delete(self, channel, ts, as_user=False):
        """
        Delete a message
        
        :param channel: The channel ID
        :type channel: str
        :param ts: Timestamp of the message to be deleted
        :type ts: str
        :param as_user: Deletes the message as the authed user
        :type as_user: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('chat.delete',
                         data={
                             'channel': channel,
                             'ts': ts,
                             'as_user': str(as_user).lower()
                         })

    def post_ephemeral(self, channel, text, user, as_user=False,
                       attachments=None, link_names=True, parse=None):
        """
        Sends an ephemeral message to a user in a channel
        
        :param channel: The channel ID
        :type channel: str
        :param text: Text of the message to send
        :type text: str
        :param user: The user ID
        :type user: str
        :param as_user: Posts the message as the authed user
        :type as_user: bool
        :param attachments: JSON array of structured attachments
        :type attachments: JSON
        :param link_names: Link channel names and users
        :type link_names: str
        :param parse: Change how messages are treated
        :type parse: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # Ensure attachments are json encoded
        if attachments is not None and isinstance(attachments, list):
            attachments = json.dumps(attachments)
        return self.post('chat.postEphemeral',
                         data={
                             'channel': channel,
                             'text': text,
                             'user': user,
                             'as_user': str(as_user).lower(),
                             'attachments': attachments,
                             'link_names': str(link_names).lower(),
                             'parse': str(parse).lower(),
                         })

    def unfurl(self, channel, ts, unfurls, user_auth_message=None,
               user_auth_required=False, user_auth_url=None):
        """
        Provides custom unfurl behavior for user posted URLS
        
        :param channel: The channel ID
        :type channel: str
        :param ts: Timestamp of the message to add unfurl behavior
        :type ts: str
        :param unfurls: JSON map with keys set to URLS in the message
        :type unfurls: JSON
        :param user_auth_message: Invitation to user to use Slack app 
        :type user_auth_message: str
        :param user_auth_required: Slack app required
        :type user_auth_required: bool
        :param user_auth_unfurl: URL for completion
        :type user_auth_unfurl: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('chat.unfurl',
                         data={
                             'channel': channel,
                             'ts': ts,
                             'unfurls': unfurls,
                             'user_auth_message': user_auth_message,
                             'user_auth_required': int(user_auth_required),
                             'user_auth_url': user_auth_url,
                         })

    def get_permalink(self, channel, message_ts):
        """
        Retrieve a permalink URL for a specific extant message
        
        :param channel:
        :type channel:
        :param message_ts:
        :type message_ts:
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('chat.getPermalink',
                        params={
                            'channel': channel,
                            'message_ts': message_ts
                        })


class IM(BaseAPI):
    def list(self):
        """
        Lists direct messages for the calling user
        
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('im.list')

    def history(self, channel, latest=None, oldest=None, count=None,
                inclusive=True, unreads=False):
        """
        Fetches history of messages and events from a DM channel
        
        :param channel: The channel ID
        :type channel: str
        :param latest: End of time range of messages to include in results
        :type latest: str
        :param oldest: Start of time range of messages to include in results
        :type oldest: str
        :param count: Number of messages to return
        :type count: int
        :param inclusive: Include messages with oldest/latest inclusive
        :type inclusive: bool
        :param unreads: Include unread count display
        :type unreads: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('im.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'count': count,
                            'inclusive': int(inclusive),
                            'unreads' : int(unreads)
                        })

    def replies(self, channel, thread_ts):
        """
        Retrieves a thread of messages posted to a DM
        
        :param channel: The channel ID
        :type channel: str
        :param thread_ts: Unique ID of thread's parent message
        :type thread_ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('im.replies',
                        params={'channel': channel, 'thread_ts': thread_ts})

    def mark(self, channel, ts):
        """
        Sets the read cursor in a DM 
         
        :param channel: The channel ID
        :type channel: str
        :param ts: Timestamp of the most recently seen message
        :type ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('im.mark', data={'channel': channel, 'ts': ts})

    def open(self, user, include_locale=True, return_im=True):
        """
        Opens a DM channel 
        
        :param user:  User to open a DM channel with
        :type user: str
        :param include_locale: Receive locales for this DM
        :type include_locale: str
        :param return_im: Return the full IM channel definition
        :type return_im: True
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('im.open', data={'user': user, 
            'include_locale': str(include_locale).lower(), 'return_im': str(return_im).lower()})

    def close(self, channel):
        """
        Close a DM channel 
        
        :param channel:
        :type channel:
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('im.close', data={'channel': channel})


class MPIM(BaseAPI):
    def open(self, users=[]):
        """
        Opens a MPIM with a list of users
        
        :param users: A list of user IDs
        :type users: list[str]
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        return self.post('mpim.open', data={'users': users})

    def close(self, channel):
        """
        Closes a MPIM
        
        :param channel: the channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('mpim.close', data={'channel': channel})

    def mark(self, channel, ts):
        """
        Sets the read cursor in a MPIM
        
        :param channel: The channel ID
        :type channel: str
        :param ts: The timestamp of the message
        :type ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('mpim.mark', data={'channel': channel, 'ts': ts})

    def list(self):
        """
        Lists MPIM for the calling user
        
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('mpim.list')

    def history(self, channel, latest=None, oldest=None, inclusive=False,
                count=None, unreads=False):
        """
        Fetches a history of messages and events
        
        :param channel: The channel ID
        :type channel: str
        :param latest: End of time range to include in results
        :type latest: str
        :param oldest: Start of time range to include in results
        :type oldest: str
        :param inclusive: Include latest/oldest messags
        :type inclusive: str
        :param count: Number of messages to return
        :type count: int
        :param unreads: Include count display
        :type unreads: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('mpim.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'inclusive': int(inclusive),
                            'count': count,
                            'unreads': int(unreads)
                        })

    def replies(self, channel, thread_ts):
        """
        Retrieves a thread of messages posted to MPIM
        
        :param channel: The channel ID
        :type channel: str
        :param thread_ts: Thread's parent message
        :type thread_ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('mpim.replies',
                        params={'channel': channel, 'thread_ts': thread_ts})


class Search(BaseAPI):
    def all(self, query, sort=None, sort_dir=None, highlight=True, count=None,
            page=None):
        """
        Searches for messages and files matching a query
        
        :param query: Search query
        :type query: str
        :param sort: Sort by score or timestamp
        :type sort: str
        :param sort_dir: Sort direction asc or desc
        :type sort_dir: str
        :param highlight: Enable highlight markers
        :type highlight: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('search.all',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': str(highlight).lower(),
                            'count': count,
                            'page': page
                        })

    def files(self, query, sort=None, sort_dir=None, highlight=True,
              count=None, page=None):
        """
        Searches for files matching a query
        
        :param query: Search query
        :type query: str
        :param sort: Sort by score or timestamp
        :type sort: str
        :param sort_dir: Sort direction asc or desc
        :type sort_dir: str
        :param highlight: Enable highlight markers
        :type highlight: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('search.files',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': str(highlight).lower(),
                            'count': count,
                            'page': page
                        })

    def messages(self, query, sort=None, sort_dir=None, highlight=True,
                 count=None, page=None):
        """
        Searches for messages matching a query
        
        :param query: Search query
        :type query: str
        :param sort: Sort by score or timestamp
        :type sort: str
        :param sort_dir: Sort direction asc or desc
        :type sort_dir: str
        :param highlight: Enable highlight markers
        :type highlight: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('search.messages',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': str(highlight).lower(),
                            'count': count,
                            'page': page
                        })


class FilesComments(BaseAPI):
    def add(self, file_, comment):
        """
        DEPRECATED - Adds a comment to a file
        
        :param file_: The file ID
        :type file_: str
        :param comment: Text of the comment
        :type comment: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.comments.add',
                         data={'file': file_, 'comment': comment})

    def delete(self, file_, id):
        """
        Deletes a comment on a file
        
        :param file_: File to delete a comment from
        :type file_: str
        :param id: The comment ID
        :type id: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.comments.delete',
                         data={'file': file_, 'id': id})

    def edit(self, file_, id, comment):
        """
        DEPRECATED - Edits a comment to a file
        
        :param file_: File to delete a comment from
        :type file_: str
        :param id: The comment ID
        :type id: str
        :param comment: Text of the comment
        :type comment: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.comments.edit',
                         data={'file': file_, 'id': id, 'comment': comment})


class Files(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Files, self).__init__(*args, **kwargs)
        self._comments = FilesComments(*args, **kwargs)

    @property
    def comments(self):
        return self._comments

    def list(self, user=None, ts_from=None, ts_to=None, types=None,
             count=None, page=None, channel=None):
        """
        List of files within a team
        
        :param user: Filter files to this user ID
        :type user: str
        :param ts_from: Timestamp from = after
        :type ts_from: str
        :param ts_to: Timestamp to = before
        :type ts_to: str
        :param types: Filter files by type
        :type types: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :param channel: Filter files to this channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('files.list',
                        params={
                            'user': user,
                            'ts_from': ts_from,
                            'ts_to': ts_to,
                            'types': types,
                            'count': count,
                            'page': page,
                            'channel': channel
                        })

    def info(self, file_, count=None, page=None, cursor=None, limit=100):
        """
        Gents information about a file
        
        :param file_: The file ID
        :type file_: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :param cursor: The parameter for pagination
        :type cursor: str
        :param limit: Max number of items to return
        :type limit: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('files.info',
                        params={'file': file_, 'count': count, 'page': page, 
                            'cursor': cursor, 'limit': limit})

    def upload(self, file_=None, content=None, filetype=None, filename=None,
               title=None, initial_comment=None, channels=None, thread_ts=None):
        """
        Uploads or creates a file
        
        :param file_: The file ID
        :type file_: str
        :param content: File contents via a POST variable
        :type content: binary
        :param filetype: File type identifier
        :type filetype: str
        :param filename: File name
        :type filename: str
        :param title: Title of the file
        :type title: str
        :param initial_comment: Comment on the file
        :type initial_comment: str
        :param channels: CSV of channel names to post to
        :type channels: list[str]
        :param thread_ts: Parent thread to use in a reply
        :type thread_ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        data = {
            'content': content,
            'filetype': filetype,
            'filename': filename,
            'title': title,
            'initial_comment': initial_comment,
            'channels': channels,
            'thread_ts': thread_ts
        }

        if file_:
            if isinstance(file_, str):
                with open(file_, 'rb') as f:
                    return self.post(
                        'files.upload', data=data, files={'file': f}
                    )

            return self.post(
                'files.upload', data=data, files={'file': file_}
            )
        else:
            return self.post('files.upload', data=data)

    def delete(self, file_):
        """
        Deletes a file
        
        :param file_: The file ID
        :type file_: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.delete', data={'file': file_})

    def revoke_public_url(self, file_):
        """
        Revokes public sharing
        
        :param file_: The file ID
        :type file_: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.revokePublicURL', data={'file': file_})

    def shared_public_url(self, file_):
        """
        Enables public sharing
        
        :param file_: The file ID
        :type file_: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.sharedPublicURL', data={'file': file_})


class Stars(BaseAPI):
    def add(self, file_=None, file_comment=None, channel=None, timestamp=None):
        """
        Adds a star to an item
        
        :param file_: The file ID
        :type file_: str
        :param file_comment: The comment on the file
        :type file_comment: str
        :param channel: The channel ID
        :type channel: str
        :param timestamp: The timestamp of the message
        :type timestamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        assert file_ or file_comment or channel

        return self.post('stars.add',
                         data={
                             'file': file_,
                             'file_comment': file_comment,
                             'channel': channel,
                             'timestamp': timestamp
                         })

    def list(self, user=None, count=None, page=None):
        """
        Lists stars for a user
        
        :param :
        :type :
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('stars.list',
                        params={'user': user, 'count': count, 'page': page})

    def remove(self, file_=None, file_comment=None, channel=None, timestamp=None):
        """
        Removes a star from an item
        
        :param file_: The file ID
        :type file_: str
        :param file_comment: The comment on the file
        :type file_comment: str
        :param channel: The channel ID
        :type channel: str
        :param timestamp: The timestamp of the message
        :type timestamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        assert file_ or file_comment or channel

        return self.post('stars.remove',
                         data={
                             'file': file_,
                             'file_comment': file_comment,
                             'channel': channel,
                             'timestamp': timestamp
                         })


class Emoji(BaseAPI):
    def list(self):
        """
        List all emojis
        
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('emoji.list')


class Presence(BaseAPI):
    AWAY = 'away'
    ACTIVE = 'active'
    TYPES = (AWAY, ACTIVE)

    def set(self, presence):
        """
        DEPRECATED - Sets the precense of a user
        
        :param presence: The status
        :type presence: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        assert presence in Presence.TYPES, 'Invalid presence type'
        return self.post('presence.set', data={'presence': presence})


class RTM(BaseAPI):
    def start(self, simple_latest=True, no_unreads=False, mpim_aware=False):
        """
        Start a Real Time Messaging session
        
        :param simple_latest: Return timestamp only for latest message object
        :type simple_latest: bool
        :param no_unreads: Skip unread counts
        :type no_unreads: bool
        :param mpim_aware: Returns MPIMs to the client
        :type mpim_aware: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('rtm.start',
                        params={
                            'simple_latest': str(simple_latest).lower(),
                            'no_unreads': str(no_unreads).lower(),
                            'mpim_aware': str(mpim_aware).lower(),
                        })

    def connect(self):
        """
        Start a Real Time Messaging session
        
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('rtm.connect')


class TeamProfile(BaseAPI):
    def get(self, visibility=None):
        """
        Retrieves a team's profile
        
        :param visibility: Filter by visibility
        :type visibility: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return super(TeamProfile, self).get(
            'team.profile.get',
            params={'visibility': str(visibility).lower()}
        )


class Team(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Team, self).__init__(*args, **kwargs)
        self._profile = TeamProfile(*args, **kwargs)

    @property
    def profile(self):
        return self._profile

    def info(self):
        """
        Gets information about the current team
        
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('team.info')

    def access_logs(self, count=None, page=None, before=None):
        """
        Gets the access log for the current team
        
        :param count: Number of items to return in the page
        :type count: int
        :param page: The page number of results
        :type page: int
        :param before: End time range of logs to include
        :type before: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('team.accessLogs',
                        params={
                            'count': count,
                            'page': page,
                            'before': before
                        })

    def integration_logs(self, service_id=None, app_id=None, user=None,
                         change_type=None, count=None, page=None):
        """
        Gets the integration logs for the current team
        
        :param service_id: Filter logs to this service
        :type service_id: str
        :param app_id: Filter logs to this slack app
        :type app_id: str
        :param user: Filter logs generated by this user
        :type user: str
        :param change_type: Filter logs to this change type
        :type change_type: str
        :param count: Number of items to return per page
        :type count: int
        :param page: The page number of results
        :type page: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('team.integrationLogs',
                        params={
                            'service_id': service_id,
                            'app_id': app_id,
                            'user': user,
                            'change_type': change_type,
                            'count': count,
                            'page': page,
                        })

    def billable_info(self, user=None):
        """
        Gets billable users information 
        
        :param user:
        :type user:
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('team.billableInfo', params={'user': user})


class Reactions(BaseAPI):
    def add(self, name, file_=None, file_comment=None, channel=None,
            timestamp=None):
        """
        Adds a reaction to an item        
        
        :param name: Reaction name
        :type name: str
        :param file_: File to add reaction to 
        :type file_: str
        :param file_comment: File comment to add reaction to 
        :type file_comment: str
        :param channel: Channel where the message to add reaction
        :type channel: str
        :param timestamp: Timestamp of the message
        :type timestamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # One of file, file_comment, or the combination of channel and timestamp
        # must be specified
        assert (file_ or file_comment) or (channel and timestamp)

        return self.post('reactions.add',
                         data={
                             'name': name,
                             'file': file_,
                             'file_comment': file_comment,
                             'channel': channel,
                             'timestamp': timestamp,
                         })

    def get(self, file_=None, file_comment=None, channel=None, timestamp=None,
            full=None):
        """
        Gets reactions for an item
        
        :param file_: File to get reaction
        :type file_: str
        :param file_comment: File comment to get reaction
        :type file_comment: str
        :param channel: Channel where the message to get reaction
        :type channel: str
        :param timestamp: Timestamp of the message
        :type timestamp: str
        :param full: Return complete reaction list
        :type full: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return super(Reactions, self).get('reactions.get',
                                          params={
                                              'file': file_,
                                              'file_comment': file_comment,
                                              'channel': channel,
                                              'timestamp': timestamp,
                                              'full': full,
                                          })

    def list(self, user=None, full=None, count=None, page=None):
        """
        List reactions made by a user
        
        :param user: User ID to list reactions
        :type user: str
        :param full: Return complete reaction list
        :type full: str
        :param count: Number of items to return on the page
        :type count: int
        :param page: Page number of results
        :type page: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return super(Reactions, self).get('reactions.list',
                                          params={
                                              'user': user,
                                              'full': full,
                                              'count': count,
                                              'page': page,
                                          })

    def remove(self, name, file_=None, file_comment=None, channel=None,
               timestamp=None):
        """
        Removes a reaction from an item
        
        :param name: Reaction name
        :type name: str
        :param file_: File to remove reaction
        :type file_: str
        :param file_comment: File comment to remove reaction
        :type file_comment: str
        :param channel: Channel where the message to remove reaction
        :type channel: str
        :param timestamp: Timestamp of the message
        :type timestamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # One of file, file_comment, or the combination of channel and timestamp
        # must be specified
        assert (file_ or file_comment) or (channel and timestamp)

        return self.post('reactions.remove',
                         data={
                             'name': name,
                             'file': file_,
                             'file_comment': file_comment,
                             'channel': channel,
                             'timestamp': timestamp,
                         })


class Pins(BaseAPI):
    def add(self, channel, file_=None, file_comment=None, timestamp=None):
        """
        Pins an item to a channel
        
        :param channel: The channel ID
        :type channel: str
        :param file_: The File ID to add
        :type file_: str
        :param file_comment: The file comment ID to add
        :type file_comment: str
        :param timestamp: Timestamp of the message to add
        :type timestamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # One of file, file_comment, or timestamp must also be specified
        assert file_ or file_comment or timestamp

        return self.post('pins.add',
                         data={
                             'channel': channel,
                             'file': file_,
                             'file_comment': file_comment,
                             'timestamp': timestamp,
                         })

    def remove(self, channel, file_=None, file_comment=None, timestamp=None):
        """
        Un-pins an item from a channel
        
        :param channel: The channel ID
        :type channel: str
        :param file_: The File ID to remove
        :type file_: str
        :param file_comment: The file comment ID to remove
        :type file_comment: str
        :param timestamp: Timestamp of the message to remove
        :type timestamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # One of file, file_comment, or timestamp must also be specified
        assert file_ or file_comment or timestamp

        return self.post('pins.remove',
                         data={
                             'channel': channel,
                             'file': file_,
                             'file_comment': file_comment,
                             'timestamp': timestamp,
                         })

    def list(self, channel):
        """
        Lists items pinned to a channel
        
        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('pins.list', params={'channel': channel})


class UserGroupsUsers(BaseAPI):
    def list(self, usergroup, include_disabled=False):
        """
        Lists all users in a usergroup
        
        :param usergroup: The usergroup ID
        :type usergroup: str
        :param include_disabled: Include disabled users
        :type include_disabled: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(include_disabled, bool):
            include_disabled = str(include_disabled).lower()

        return self.get('usergroups.users.list', params={
            'usergroup': usergroup,
            'include_disabled': include_disabled,
        })

    def update(self, usergroup, users, include_count=False):
        """
        Updates the list of users for a usergroup
        
        :param usergroup: The usergroup ID
        :type usergroup: str
        :param users: CSV of user IDs to add
        :type users: list[str]
        :param include_count: Include a count of users
        :type include_count: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        return self.post('usergroups.users.update', data={
            'usergroup': usergroup,
            'users': users,
            'include_count': str(include_count).lower(),
        })


class UserGroups(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(UserGroups, self).__init__(*args, **kwargs)
        self._users = UserGroupsUsers(*args, **kwargs)

    @property
    def users(self):
        return self._users

    def list(self, include_disabled=False, include_count=False, include_users=False):
        """
        Lists all of the usergroups 
        
        :param include_disabled: Include disabled usergroups
        :type include_disabled: bool
        :param include_count: Include the number of users in the usergroup
        :type include_count: bool
        :param include_users: Include the list of users of the usergroup
        :type include_users: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('usergroups.list', params={
            'include_disabled': str(include_disabled).lower(),
            'include_count': str(include_count).lower(),
            'include_users': str(include_users).lower(),
        })

    def create(self, name, handle=None, description=None, channels=None,
               include_count=False):
        """
        Creates a new usergroup 
        
        :param name: A name for the usergroup
        :type name: str
        :param handle: The mention handle
        :type handle: str
        :param description: Description of the usergroup
        :type description: str
        :param channels: CSV of channel IDs for the usergroup
        :type channels: list[str]
        :param include_count: Include the number of users in the usergroup
        :type include_count: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        return self.post('usergroups.create', data={
            'name': name,
            'handle': handle,
            'description': description,
            'channels': channels,
            'include_count': str(include_count).lower(),
        })

    def update(self, usergroup, name=None, handle=None, description=None,
               channels=None, include_count=True):
        """
        Update an existing usergroup
        
        :param usergroup: The encoded ID of the usergroup
        :type usergroup: str
        :param name: A name for the usergroup
        :type name: str
        :param handle: The mention handle
        :type handle: str
        :param description: Description of the usergroup
        :type description: str
        :param channels: CSV of channel IDs for the usergroup
        :type channels: list[str]
        :param include_count: Include the number of users in the usergroup
        :type include_count: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        return self.post('usergroups.update', data={
            'usergroup': usergroup,
            'name': name,
            'handle': handle,
            'description': description,
            'channels': channels,
            'include_count': str(include_count).lower(),
        })

    def disable(self, usergroup, include_count=True):
        """
        Disable a UserGroup
        
        :param usergroup: The encoded ID of the usergroup
        :type usergroup: str
        :param include_count: Include the number of users
        :type include_count: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('usergroups.disable', data={
            'usergroup': usergroup,
            'include_count': str(include_count).lower(),
        })

    def enable(self, usergroup, include_count=True):
        """
        Enable a UserGroup
        
        :param usergroup: The encoded ID of the usergroup
        :type usergroup: str
        :param include_count: Include the number of users
        :type include_count: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('usergroups.enable', data={
            'usergroup': usergroup,
            'include_count': str(include_count).lower(),
        })


class DND(BaseAPI):
    def team_info(self, users=[]):
        """
        Provides info about DND for a list of users on a Slack team
        
        :param users: The list of user ids
        :type users: list[str]
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        return self.get('dnd.teamInfo', params={'users': users})

    def set_snooze(self, num_minutes):
        """
        The number of minutes to snooze
        
        :param num_minutes: The number of minutes to snooze
        :type num_minutes: int
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('dnd.setSnooze', data={'num_minutes': num_minutes})

    def info(self, user=None):
        """
        Retrieves the current user's DND status
        
        :param user: User ID to fetch status
        :type user: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('dnd.info', params={'user': user})

    def end_dnd(self):
        """
        Ends the current user's DND session
        
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('dnd.endDnd')

    def end_snooze(self):
        """
        End's the current user's snooze
        
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('dnd.endSnooze')


class Reminders(BaseAPI):
    def add(self, text, time, user=None):
        """
        Creates a reminder
        
        :param text: Content of the reminder
        :type text: str
        :param time: Unix timestamp to show the reminder
        :type time: int
        :param user: User ID attached to the reminder
        :type user: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('reminders.add', data={
            'text': text,
            'time': time,
            'user': user,
        })

    def complete(self, reminder):
        """
        Mark the reminder as completed
        
        :param reminder: The reminder ID
        :type reminder: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('reminders.complete', data={'reminder': reminder})

    def delete(self, reminder):
        """
        Deletes a reminder
        
        :param reminder: The reminder ID
        :type reminder: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('reminders.delete', data={'reminder': reminder})

    def info(self, reminder):
        """
        Returns information about a reminder
        
        :param reminder: The reminder ID
        :type reminder: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('reminders.info', params={'reminder': reminder})

    def list(self):
        """
        Returns a list of reminders created by or for a given user
        
        :param :
        :type :
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('reminders.list')


class Bots(BaseAPI):
    def info(self, bot=None):
        """
        Gets information about a bot user
        
        :param bot: Bot user ID
        :type bot: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('bots.info', params={'bot': bot})


class IDPGroups(BaseAPI):
    def list(self, include_users=False):
        """
        DEPRECATED? This class will be removed in the next major release.
        
        :param :
        :type :
        :return :
        :rtype:
        """
        return self.get('idpgroups.list',
                        params={'include_users': int(include_users)})


class OAuth(BaseAPI):
    def access(self, client_id, client_secret, code, redirect_uri=None):
        """
        Exchanges a temporary OAuth verifier code for an access token 
        
        :param client_id: Issued when you created your application
        :type client_id: str
        :param client_secret: Issued when you created your application.
        :type client_secret: str
        :param code: Code para returned via the callback
        :type code: str
        :param redirect_uri: URL to land on
        :type redirect_uri: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('oauth.access',
                         data={
                             'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'redirect_uri': redirect_uri
                         })

    def token(self, client_id, client_secret, code, redirect_uri=None,
              single_channel=None):
        """
        Exchanges a temporary OAuth verifier code for a workspace token 
        
        :param client_id: Issued when you created your application
        :type client_id: str
        :param client_secret: Issued when you created your application.
        :type client_secret: str
        :param code: Code para returned via the callback
        :type code: str
        :param redirect_uri: URL to land on
        :type redirect_uri: str
        :param single_channel: Request the user to add the app only to a single channel
        :type single_channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('oauth.token',
                         data={
                             'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'redirect_uri': redirect_uri,
                             'single_channel': single_channel,
                         })


class AppsPermissions(BaseAPI):
    def info(self):
        """
        All current permissions this app has (deprecated)

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('apps.permissions.info')

    def request(self, scopes, trigger_id):
        """
        All current permissions this app has

        :param scopes: A comma separated list of scopes to request for
        :type scopes: list[str]
        :param trigger_id: Token used to trigger the permissions API
        :type trigger_id: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('apps.permissions.request',
                         data={
                             scopes: ','.join(scopes),
                             trigger_id: trigger_id,
                         })


class Apps(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Apps, self).__init__(*args, **kwargs)
        self._permissions = AppsPermissions(*args, **kwargs)

    @property
    def permissions(self):
        return self._permissions


class IncomingWebhook(object):
    def __init__(self, url=None, timeout=DEFAULT_TIMEOUT, proxies=None):
        self.url = url
        self.timeout = timeout
        self.proxies = proxies

    def post(self, data):
        """
        Posts message with payload formatted in accordance with
        this documentation https://api.slack.com/incoming-webhooks

        :param data: The data payload
        :type data: A JSON representation of the payload
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        if not self.url:
            raise Error('URL for incoming webhook is undefined')

        return requests.post(self.url, data=json.dumps(data),
                             timeout=self.timeout, proxies=self.proxies)


class Slackest(object):
    oauth = OAuth(timeout=DEFAULT_TIMEOUT)

    def __init__(self, token, incoming_webhook_url=None,
                 timeout=DEFAULT_TIMEOUT, http_proxy=None, https_proxy=None,
                 session=None, rate_limit_retries=DEFAULT_RETRIES):

        proxies = self.__create_proxies(http_proxy, https_proxy)
        api_args = {
            'token': token,
            'timeout': timeout,
            'proxies': proxies,
            'session': session,
            'rate_limit_retries': rate_limit_retries,
        }
        self.im = IM(**api_args)
        self.api = API(**api_args)
        self.dnd = DND(**api_args)
        self.rtm = RTM(**api_args)
        self.apps = Apps(**api_args)
        self.auth = Auth(**api_args)
        self.bots = Bots(**api_args)
        self.conversation = Conversation(**api_args)
        self.chat = Chat(**api_args)
        self.dialog = Dialog(**api_args)
        self.team = Team(**api_args)
        self.pins = Pins(**api_args)
        self.mpim = MPIM(**api_args)
        self.users = Users(**api_args)
        self.files = Files(**api_args)
        self.stars = Stars(**api_args)
        self.emoji = Emoji(**api_args)
        self.search = Search(**api_args)
        self.groups = Groups(**api_args)
        self.channels = Channels(**api_args)
        self.presence = Presence(**api_args)
        self.reminders = Reminders(**api_args)
        self.reactions = Reactions(**api_args)
        self.idpgroups = IDPGroups(**api_args)
        self.usergroups = UserGroups(**api_args)
        self.incomingwebhook = IncomingWebhook(url=incoming_webhook_url,
                                               timeout=timeout, proxies=proxies)

    def __create_proxies(self, http_proxy=None, https_proxy=None):
        """
        Creates the appropriate proxy type

        :param http_proxy: An HTTP proxy
        :type http_proxy: bool
        :param https_proxy: An HTTPS proxy
        :type https_proxy: bool
        :return: A dictionary of proxy configurations
        :rtype: dict
        """
        proxies = dict()
        if http_proxy:
            proxies['http'] = http_proxy
        if https_proxy:
            proxies['https'] = https_proxy
        return proxies

    def create_channel(self, name, is_private=True, users=[]):
        """
        Creates a channel

        :param name: The channel name
        :type name: str
        :param is_private: Determines if channel is private (like a group)
        :type is_private: bool
        :param user_ids: A list of User IDs to add to the channel
        :type user_ids: list[str]
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.create(name, is_private, users)

    def get_channels(self, exclude_archive, types):
        """
        Lists all channels

        :param exclude_archived: Exclude archived channels
        :type exclude_archived: bool
        :param types: The type of channel to return, can be one of public_channel, private_channel
        :type types: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.list_all(exclude_archived=exclude_archive, types=types)

    def list_all_users(self):
        """
        Lists all users

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.users.list_all(include_locale=True)

    def kick_user(self, channel, user):
        """
        Removes a user from a channel

        :param channel: The channel ID
        :type channel: str
        :param user: The user ID
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.kick(channel, user)

    def history_all(self, channel):
        """
        Fetches all history of messages and events from a channel

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.history_all(channel)

    def post_message_to_channel(self, channel, message):
        """
        Posts a message to a channel

        :param channel: The channel ID
        :type channel: str
        :param message: The message text
        :type message: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.chat.post_message(channel, text=message, link_names=True)

    def post_thread_to_message(self, channel, message, thread_ts):
        """

        :param channel: The channel ID
        :type channel: str
        :param message: The message text
        :type message: str
        :param thread_ts: The parent thread timestamp identifier
        :type thread_ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.chat.post_message(channel, text=message, thread_ts=thread_ts, link_names=True)

    def add_member_to_channel(self,channel, member):
        """
        Invites a user to a channel

        :param channel: The channel ID
        :type channel: str
        :param user: A user ID to invite to a channel
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.invite(channel, member)

    def get_channel_info(self, channel):
        """
        Gets information about a channel.

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.channels.info(channel)

    def get_replies(self, channel, ts):
        """
        Fetches all replies in a thread of messages

        :param channel: The channel ID
        :type channel: str
        :param ts: Unique identifier of a thread's parent message
        :type ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.replies_all(channel, ts)

    def set_purpose(self, channel, purpose):
        """
        Sets the purpose a channel

        :param channel: The channel ID
        :type channel: str
        :param purpose: The purpose to set
        :type purpose: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.setPurpose(channel, purpose)

    def set_topic(self, channel, topic):
        """
        Sets the topic a channel

        :param channel: The channel ID
        :type channel: str
        :param topic: The topic to set
        :type topic: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.setTopic(channel, topic)

    def upload_file(self, filename, channels):
        """
        Uploads a file to a channel

        :param filename: The filename to upload
        :type filename: str
        :param channels: Channel IDs to upload to
        :type channels: list[str]
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.files.upload(filename, channels=channels)
