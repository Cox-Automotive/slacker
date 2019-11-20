from .base_api import BaseAPI

class Stars(BaseAPI):
    """Follows the Slack Stars API. See https://api.slack.com/methods"""

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
        yield self.get('stars.list',
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
