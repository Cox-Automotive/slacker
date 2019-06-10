from .base_api import BaseAPI

class AppsPermissions(BaseAPI):
    """Follows the Slack AppsPermissions API. See https://api.slack.com/methods"""

    def info(self):
        """
        All current permissions this app has (deprecated)

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('apps.permissions.info')

    def request(self, scopes, trigger_id):
        """
        All current permissions this app has

        :param scopes: A comma separated list of scopes to request for
        :type scopes: list[str]
        :param trigger_id: Token used to trigger the permissions API
        :type trigger_id: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('apps.permissions.request',
                         data={
                             scopes: ','.join(scopes),
                             trigger_id: trigger_id,
                         })

