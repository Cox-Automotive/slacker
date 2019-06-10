from .base_api import BaseAPI

class UsersProfile(BaseAPI):
    """Follows the Slack UsersProfile API. See https://api.slack.com/methods"""

    def get(self, user=None, include_labels=False):
        """
        Gets a Slack user's profile

        :param user: User to retrieve profile info for
        :type user: str
        :param include_labels: Include labels for each ID in custom profile fields
        :type include_labels: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return super(UsersProfile, self).get(
            'users.profile.get',
            params={'user': user, 'include_labels': str(include_labels).lower()}
        )

    def set(self, user=None, profile=None, name=None, value=None):
        """
        Gets a Slack user's profile

        :param user: ID of user to change
        :type user: str
        :param profile: Collection of key:value pairs presented as a URL-encoded JSON hash
        :type profile: str
        :param name: Name of a single key to set
        :type name: str
        :param value: Value to set a single key to
        :type value: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('users.profile.set',
                         data={
                             'user': user,
                             'profile': profile,
                             'name': name,
                             'value': value
                         })
