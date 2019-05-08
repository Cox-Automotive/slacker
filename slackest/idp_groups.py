from .base_api import BaseAPI

class IDPGroups(BaseAPI):
    """Follows the Slack IDPGroups API. See https://api.slack.com/methods"""

    def list(self, include_users=False):
        """
        DEPRECATED? This class will be removed in the next major release.

        :param :
        :type :
        :return :
        :rtype:
        """
        return self.get('idpgroups.list',
                        params={'include_users': int(include_users)})

