from .base_api import BaseAPI

class IM(BaseAPI):
    """Follows the Slack IM API. See https://api.slack.com/methods"""

    def list(self):
        """
        Lists direct messages for the calling user

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        yield self.get('im.list')

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

    def mark(self, channel, time_stamp):
        """
        Sets the read cursor in a DM

        :param channel: The channel ID
        :type channel: str
        :param time_stamp: Timestamp of the most recently seen message
        :type time_stamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('im.mark', data={'channel': channel, 'ts': time_stamp})

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
        return self.post('im.open',
                         data={'user': user, 'include_locale': str(include_locale).lower(),
                               'return_im': str(return_im).lower()})

    def close(self, channel):
        """
        Close a DM channel

        :param channel:
        :type channel:
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('im.close', data={'channel': channel})
