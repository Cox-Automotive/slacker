from .base_api import BaseAPI

class TeamProfile(BaseAPI):
    """Follows the Slack TeamProfile API. See https://api.slack.com/methods"""

    def get(self, visibility=None):
        """
        Retrieves a team's profile

        :param visibility: Filter by visibility
        :type visibility: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return super(TeamProfile, self).get(
            'team.profile.get',
            params={'visibility': str(visibility).lower()}
        )
