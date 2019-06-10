from .base_api import BaseAPI

class Bots(BaseAPI):
    """Follows the Slack Bots API. See https://api.slack.com/methods"""

    def info(self, bot=None):
        """
        Gets information about a bot user

        :param bot: Bot user ID
        :type bot: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('bots.info', params={'bot': bot})

