from .base_api import BaseAPI

class Emoji(BaseAPI):
    """Follows the Slack Emoji API. See https://api.slack.com/methods"""

    def list(self):
        """
        List all emojis

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('emoji.list')
