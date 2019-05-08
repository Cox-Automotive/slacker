from .base_api import BaseAPI

class DND(BaseAPI):
    """Follows the Slack DND API. See https://api.slack.com/methods"""

    def team_info(self, users=[]):
        """
        Provides info about DND for a list of users on a Slack team

        :param users: The list of user ids
        :type users: list[str]
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        return self.get('dnd.teamInfo', params={'users': users})

    def set_snooze(self, num_minutes):
        """
        The number of minutes to snooze

        :param num_minutes: The number of minutes to snooze
        :type num_minutes: int
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('dnd.setSnooze', data={'num_minutes': num_minutes})

    def info(self, user=None):
        """
        Retrieves the current user's DND status

        :param user: User ID to fetch status
        :type user: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('dnd.info', params={'user': user})

    def end_dnd(self):
        """
        Ends the current user's DND session

        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('dnd.endDnd')

    def end_snooze(self):
        """
        End's the current user's snooze

        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('dnd.endSnooze')

