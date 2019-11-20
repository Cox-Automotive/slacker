from .base_api import BaseAPI

class Pins(BaseAPI):
    """Follows the Slack Pins API. See https://api.slack.com/methods"""

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
        yield self.get('pins.list', params={'channel': channel})

