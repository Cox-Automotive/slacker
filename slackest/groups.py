from .base_api import BaseAPI

class Groups(BaseAPI):
    """Follows the Slack Groups API. See https://api.slack.com/methods"""

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
        yield self.get('groups.list',
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

    def mark(self, channel, time_stamp):
        """
        Moves the read cursor in a private channel

        :param channel: The private channel ID
        :type channel: str
        :param time_stamp: The timestamp of the most recently seen message
        :type time_stamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('groups.mark', data={'channel': channel, 'ts': time_stamp})

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
