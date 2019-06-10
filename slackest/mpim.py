from .base_api import BaseAPI

class MPIM(BaseAPI):
    """Follows the Slack MPIM API. See https://api.slack.com/methods"""

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

    def mark(self, channel, time_stamp):
        """
        Sets the read cursor in a MPIM

        :param channel: The channel ID
        :type channel: str
        :param time_stamp: The timestamp of the message
        :type time_stamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('mpim.mark', data={'channel': channel, 'ts': time_stamp})

    def list(self):
        """
        Lists MPIM for the calling user

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        yield self.get('mpim.list')

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
        yield self.get('mpim.history',
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
        yield self.get('mpim.replies',
                        params={'channel': channel, 'thread_ts': thread_ts})
