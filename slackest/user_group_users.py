from .base_api import BaseAPI

class UserGroupsUsers(BaseAPI):
    """Follows the Slack UserGroupUsers API. See https://api.slack.com/methods"""

    def list(self, usergroup, include_disabled=False):
        """
        Lists all users in a usergroup

        :param usergroup: The usergroup ID
        :type usergroup: str
        :param include_disabled: Include disabled users
        :type include_disabled: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(include_disabled, bool):
            include_disabled = str(include_disabled).lower()

        yield self.get('usergroups.users.list', params={
            'usergroup': usergroup,
            'include_disabled': include_disabled,
        })

    def update(self, usergroup, users, include_count=False):
        """
        Updates the list of users for a usergroup

        :param usergroup: The usergroup ID
        :type usergroup: str
        :param users: CSV of user IDs to add
        :type users: list[str]
        :param include_count: Include a count of users
        :type include_count: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        return self.post('usergroups.users.update', data={
            'usergroup': usergroup,
            'users': users,
            'include_count': str(include_count).lower(),
        })

