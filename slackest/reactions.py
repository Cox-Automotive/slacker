from .base_api import BaseAPI

class Reactions(BaseAPI):
    """Follows the Slack Reactions API. See https://api.slack.com/methods"""

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
        yield super(Reactions, self).get('reactions.list',
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

