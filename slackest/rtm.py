from .base_api import BaseAPI

class RTM(BaseAPI):
    """Follows the Slack RTM API. See https://api.slack.com/methods"""

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
