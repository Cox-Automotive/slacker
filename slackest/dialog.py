import json

from .base_api import BaseAPI

class Dialog(BaseAPI):
    """Follows the Slack Dialog API. See https://api.slack.com/methods"""

    def open(self, dialog, trigger_id):
        """
        Opens a dialog with a user

        :param dialog: JSON-encoded dialog definition
        :type dialog: json
        :param trigger_id: The trigger to post to the user.
        :type trigger_id: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('dialog.open',
                         data={
                             'dialog': json.dumps(dialog),
                             'trigger_id': trigger_id,
                         })