from .base_api import BaseAPI

class API(BaseAPI):
    """Follows the Slack Test API. See https://api.slack.com/methods"""

    def test(self, error=None, **kwargs):
        """
        Allows access to the Slack API test endpoint

        :param error: The API error
        :type error: str
        :param kwargs: Various keyword arguments that could be passed to the request
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if error:
            kwargs['error'] = error

        return self.get('api.test', params=kwargs)