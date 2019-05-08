from .base_api import BaseAPI

class OAuth(BaseAPI):
    """Follows the Slack OAuth API. See https://api.slack.com/methods"""

    def access(self, client_id, client_secret, code, redirect_uri=None):
        """
        Exchanges a temporary OAuth verifier code for an access token

        :param client_id: Issued when you created your application
        :type client_id: str
        :param client_secret: Issued when you created your application.
        :type client_secret: str
        :param code: Code para returned via the callback
        :type code: str
        :param redirect_uri: URL to land on
        :type redirect_uri: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('oauth.access',
                         data={
                             'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'redirect_uri': redirect_uri
                         })

    def token(self, client_id, client_secret, code, redirect_uri=None,
              single_channel=None):
        """
        Exchanges a temporary OAuth verifier code for a workspace token

        :param client_id: Issued when you created your application
        :type client_id: str
        :param client_secret: Issued when you created your application.
        :type client_secret: str
        :param code: Code para returned via the callback
        :type code: str
        :param redirect_uri: URL to land on
        :type redirect_uri: str
        :param single_channel: Request the user to add the app only to a single channel
        :type single_channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('oauth.token',
                         data={
                             'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'redirect_uri': redirect_uri,
                             'single_channel': single_channel,
                         })

