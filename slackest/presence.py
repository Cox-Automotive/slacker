from .base_api import BaseAPI

class Presence(BaseAPI):
    """Follows the Slack Presence API. See https://api.slack.com/methods"""

    AWAY = 'away'
    ACTIVE = 'active'
    TYPES = (AWAY, ACTIVE)

    def set(self, presence):
        """
        DEPRECATED - Sets the precense of a user

        :param presence: The status
        :type presence: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        assert presence in Presence.TYPES, 'Invalid presence type'
        return self.post('presence.set', data={'presence': presence})
