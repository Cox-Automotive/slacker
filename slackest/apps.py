from .base_api import BaseAPI
from .apps_permissions import AppsPermissions

class Apps(BaseAPI):
    """Follows the Slack Apps API. See https://api.slack.com/methods"""

    def __init__(self, *args, **kwargs):
        super(Apps, self).__init__(*args, **kwargs)
        self._permissions = AppsPermissions(*args, **kwargs)

    @property
    def permissions(self):
        return self._permissions

