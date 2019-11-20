from .base_api import BaseAPI
from .user_group_users import UserGroupsUsers

class UserGroups(BaseAPI):
    """Follows the Slack UserGroups API. See https://api.slack.com/methods"""

    def __init__(self, *args, **kwargs):
        super(UserGroups, self).__init__(*args, **kwargs)
        self._users = UserGroupsUsers(*args, **kwargs)

    @property
    def users(self):
        return self._users

    def list(self, include_disabled=False, include_count=False, include_users=False):
        """
        Lists all of the usergroups

        :param include_disabled: Include disabled usergroups
        :type include_disabled: bool
        :param include_count: Include the number of users in the usergroup
        :type include_count: bool
        :param include_users: Include the list of users of the usergroup
        :type include_users: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        yield self.get('usergroups.list', params={
            'include_disabled': str(include_disabled).lower(),
            'include_count': str(include_count).lower(),
            'include_users': str(include_users).lower(),
        })

    def create(self, name, handle=None, description=None, channels=None,
               include_count=False):
        """
        Creates a new usergroup

        :param name: A name for the usergroup
        :type name: str
        :param handle: The mention handle
        :type handle: str
        :param description: Description of the usergroup
        :type description: str
        :param channels: CSV of channel IDs for the usergroup
        :type channels: list[str]
        :param include_count: Include the number of users in the usergroup
        :type include_count: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        return self.post('usergroups.create', data={
            'name': name,
            'handle': handle,
            'description': description,
            'channels': channels,
            'include_count': str(include_count).lower(),
        })

    def update(self, usergroup, name=None, handle=None, description=None,
               channels=None, include_count=True):
        """
        Update an existing usergroup

        :param usergroup: The encoded ID of the usergroup
        :type usergroup: str
        :param name: A name for the usergroup
        :type name: str
        :param handle: The mention handle
        :type handle: str
        :param description: Description of the usergroup
        :type description: str
        :param channels: CSV of channel IDs for the usergroup
        :type channels: list[str]
        :param include_count: Include the number of users in the usergroup
        :type include_count: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        return self.post('usergroups.update', data={
            'usergroup': usergroup,
            'name': name,
            'handle': handle,
            'description': description,
            'channels': channels,
            'include_count': str(include_count).lower(),
        })

    def disable(self, usergroup, include_count=True):
        """
        Disable a UserGroup

        :param usergroup: The encoded ID of the usergroup
        :type usergroup: str
        :param include_count: Include the number of users
        :type include_count: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('usergroups.disable', data={
            'usergroup': usergroup,
            'include_count': str(include_count).lower(),
        })

    def enable(self, usergroup, include_count=True):
        """
        Enable a UserGroup

        :param usergroup: The encoded ID of the usergroup
        :type usergroup: str
        :param include_count: Include the number of users
        :type include_count: bool
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('usergroups.enable', data={
            'usergroup': usergroup,
            'include_count': str(include_count).lower(),
        })

