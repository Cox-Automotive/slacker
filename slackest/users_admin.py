from .base_api import BaseAPI

class UsersAdmin(BaseAPI):
    """Follows the Slack UsersAdmin API. See https://api.slack.com/methods"""

    def invite(self, email, channels=None, first_name=None,
               last_name=None, resend=True):
        """
        DEPRECATED - Invites a user to channel(s) via email. Looks to be deprecated.

        :param email: Email of the user to invite to a channel(s)
        :type email: str
        :param channels: A CSV of channels for the invite.
        :type channels: str
        :param first_name: First name of the invitee
        :type first_name: str
        :param last_name: Last name of the invitee
        :type last_name: str
        :param resend: Whether or not this invite is a resend
        :type resend: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('users.admin.invite',
                         params={
                             'email': email,
                             'channels': channels,
                             'first_name': first_name,
                             'last_name': last_name,
                             'resend': resend
                         })
