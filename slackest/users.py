import time
from .base_api import BaseAPI
from .slackest_error import SlackestError
from .users_profile import UsersProfile
from .users_admin import UsersAdmin
from .utils import get_item_id_by_name
from .constants import *
from .response import Response


class Users(BaseAPI):
    """Follows the Slack Users API. See https://api.slack.com/methods"""

    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self._profile = UsersProfile(*args, **kwargs)
        self._admin = UsersAdmin(*args, **kwargs)

    @property
    def profile(self):
        """
        Returns the profile object attribute

        :return: A usersprofile object.
        :rtype: :class:`UsersProfile <UsersProfile>` object
        """
        return self._profile

    @property
    def admin(self):
        return self._admin

    def info(self, user, include_locale=False):
        """
        Returns information about the user

        :param user: The Slack user ID of the user to look up
        :type user: str
        :param include_locale: Whether or not to include the user's locale
        :type include_locale: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('users.info',
                        params={'user': user, 'include_locale': str(include_locale).lower()})

    def list(self, cursor=None, include_locale=True, limit=500):
        """
        List all users in a Slack team.

        :param cursor: Cursor pagination
        :type cursor: str
        :param include_locale: Receive the user's locale
        :type include_locale: bool
        :param limit: The maximum number of users to return
        :type limit: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        yield self.get('users.list',
                        params={'include_locale': str(include_locale).lower(),
                                'limit': limit, 'cursor': cursor})

    def list_all(self, include_locale=True):
        """
        Lists all users in a Slack team

        :param include_locale: Receive the user's locale
        :type include_locale: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        response = self.get('users.list', params={'include_locale': str(include_locale).lower()})
        members = response.body.get('members', [])
        next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
        while next_cursor:
            response = self.get('users.list',
                                params={'include_locale': str(include_locale).lower(),
                                        'cursor': next_cursor})
            if response is not None:
                members.extend(response.body.get('members', []))
                next_cursor = response.body.get('response_metadata', {}).get('next_cursor', '')
                time.sleep(DEFAULT_API_SLEEP)
            else:
                raise SlackestError("Null response received. You've probably hit the rate limit.")

        if members:
            response.body['members'] = members

        yield response

    def identity(self):
        """
        Retrieves the user's identity: name, ID, team

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('users.identity')

    def set_active(self):
        """
        Sets the user object to active. DEPRECATED

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('users.setActive')

    def get_presence(self, user):
        """
        Gets the presence of the Slack user

        :param user: The Slack user ID
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('users.getPresence', params={'user': user})

    def set_presence(self, presence):
        """
        Sets the presence of the current Slack user

        :param presence: The presence level of the user: either `auto` or `away`
        :type presence: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('users.setPresence', data={'presence': presence})

    def get_user_id(self, user_name):
        """
        Gets a user ID according to the user's name

        :param user_name: The user's name
        :type user_name: str
        :return: Returns the user ID
        :rtype: str
        """
        members_gen = next(self.list_all())
        members = members_gen.body['members']
        return get_item_id_by_name(members, user_name) 
