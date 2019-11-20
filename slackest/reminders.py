from .base_api import BaseAPI

class Reminders(BaseAPI):
    """Follows the Slack Reminders API. See https://api.slack.com/methods"""

    def add(self, text, reminder_time, user=None):
        """
        Creates a reminder

        :param text: Content of the reminder
        :type text: str
        :param reminder_time: Unix timestamp to show the reminder
        :type reminder_time: int
        :param user: User ID attached to the reminder
        :type user: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('reminders.add',
                         data={'text': text, 'time': reminder_time, 'user': user})

    def complete(self, reminder):
        """
        Mark the reminder as completed

        :param reminder: The reminder ID
        :type reminder: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('reminders.complete', data={'reminder': reminder})

    def delete(self, reminder):
        """
        Deletes a reminder

        :param reminder: The reminder ID
        :type reminder: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('reminders.delete', data={'reminder': reminder})

    def info(self, reminder):
        """
        Returns information about a reminder

        :param reminder: The reminder ID
        :type reminder: str
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('reminders.info', params={'reminder': reminder})

    def list(self):
        """
        Returns a list of reminders created by or for a given user

        :param :
        :type :
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        yield self.get('reminders.list')

