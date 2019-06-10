from .base_api import BaseAPI

class Auth(BaseAPI):
    """Follows the Slack Auth API. See https://api.slack.com/methods"""

    def test(self):
        """
        Allows access to the Slack API test endpoint

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('auth.test')

    def revoke(self, test=True):
        """
        Allows access to the Slack API test endpoint

        :param test: Boolean to run the test
        :type test: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('auth.revoke', data={'test': int(test)})