import requests
import json

from .slackest_error import SlackestError
from .constants import *

class IncomingWebhook(object):
    """Follows the Slack IncomingWebhook API. See https://api.slack.com/methods"""

    def __init__(self, url=None, timeout=DEFAULT_TIMEOUT, proxies=None):
        self.url = url
        self.timeout = timeout
        self.proxies = proxies

    def post(self, data):
        """
        Posts message with payload formatted in accordance with
        this documentation https://api.slack.com/incoming-webhooks

        :param data: The data payload
        :type data: A JSON representation of the payload
        :return: A response object to run the request.
        :rtype: :class:`Response <Response>` object
        """
        if not self.url:
            raise SlackestError('URL for incoming webhook is undefined')

        return requests.post(self.url, data=json.dumps(data),
                             timeout=self.timeout, proxies=self.proxies)