import time
import datetime
import requests

from .constants import *
from .response import Response
from .slackest_error import SlackestError



class BaseAPI(object):
    """BaseAPI interface for making the `requests` calls to Slack."""

    def __init__(self, token=None, timeout=DEFAULT_TIMEOUT, proxies=None,
                 session=None, rate_limit_retries=DEFAULT_RETRIES):
        self.token = token
        self.timeout = timeout
        self.proxies = proxies
        self.session = session
        self.rate_limit_retries = rate_limit_retries
        self.retry_max = 10
        self.retry_counter = 0
        self.retry_wait_secs = 1

    def _request(self, method, api, **kwargs):
        """
        Internal request call, with rate limiting retries

        :param method: The method to call: GET, POST, etc.
        :type method: :class:`Request <Request>` object
        :param api: The API endpoint
        :type api: str
        :param kwargs: Various keyword arguments that could be passed to the request
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if self.token:
            kwargs.setdefault('params', {})['token'] = self.token

        # while we have rate limit retries left, fetch the resource and back
        # off as Slack's HTTP response suggests
        for retry_num in range(self.rate_limit_retries):
            response = method(API_BASE_URL.format(api=api),
                              timeout=self.timeout,
                              proxies=self.proxies,
                              **kwargs)

            if response.status_code == requests.codes.ok:
                break

            # handle HTTP 429 as documented at
            # https://api.slack.com/docs/rate-limits
            elif response.status_code == requests.codes.too_many: # HTTP 429
                time.sleep(int(response.headers.get('retry-after', DEFAULT_WAIT)))
                continue
            else:
                response.raise_for_status()
        else:
            # with no retries left, make one final attempt to fetch the resource,
            # but do not handle too_many status differently
            response = method(API_BASE_URL.format(api=api),
                              timeout=self.timeout,
                              proxies=self.proxies,
                              **kwargs)
            response.raise_for_status()

        response = Response(response.text)
        if not response.successful:
            raise SlackestError(response.error)

        return response

    def _session_get(self, url, params=None, **kwargs):
        """
        Internal request GET call with session

        :param url: The URL to request
        :type url: str
        :param params: Dictionary containing URL request parameters (headers, etc.)
        :type params: dict
        :param kwargs: Various keyword arguments that could be passed to the GET
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        kwargs.setdefault('allow_redirects', True)
        return self.session.request(
            method='get', url=url, params=params, **kwargs
        )

    def _session_post(self, url, data=None, **kwargs):
        """
        Internal request POST call with session

        :param url: The URL to request
        :type url: str
        :param params: Dictionary containing request data
        :type params: dict
        :param kwargs: Various keyword arguments that could be passed to the POST
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.session.request(
            method='post', url=url, data=data, **kwargs
        )

    def get(self, api, **kwargs):
        """
        External request GET call, wraps around internal _request.get

        :param api: The API endpoint to connect to
        :type api: str
        :param kwargs: Various keyword arguments that could be passed to the GET
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        try:
            return self._request(
                self._session_get if self.session else requests.get,
                api, **kwargs
            )
        except requests.HTTPError as e:
            # Put a retry here with a short circuit
            if self.retry_counter < self.retry_max:
                self.retry_counter = self.retry_counter + 1
                time.sleep(self.retry_wait_secs)
                self.get(api, **kwargs)
            else:
                raise

    def post(self, api, **kwargs):
        """
        External request POST call, wraps around internal _request.post

        :param api: The API endpoint to connect to
        :type api: str
        :param kwargs: Various keyword arguments that could be passed to the POST
        :type kwargs: dict
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self._request(
            self._session_post if self.session else requests.post,
            api, **kwargs
        ) 