from .base_api import BaseAPI
from .utils import *

class Channels(BaseAPI):
    """Follows the Slack Channels API. See https://api.slack.com/methods"""

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
        yield self.get('channels.list',
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

    def mark(self, channel, time_stamp):
        """
        Moves the read cursor in a public channel

        :param channel: The channel ID
        :type channel: str
        :param time_stamp: The timestamp of the most recently seen message
        :type time_stamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('channels.mark',
                         data={'channel': channel, 'ts': time_stamp})

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
        channels_gen = next(self.list())
        channels = channels_gen.body['channels']
        return get_item_id_by_name(channels, channel_name)
