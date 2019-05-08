from .base_api import BaseAPI

class Search(BaseAPI):
    """Follows the Slack Search API. See https://api.slack.com/methods"""

    def all(self, query, sort=None, sort_dir=None, highlight=True, count=None,
            page=None):
        """
        Searches for messages and files matching a query

        :param query: Search query
        :type query: str
        :param sort: Sort by score or timestamp
        :type sort: str
        :param sort_dir: Sort direction asc or desc
        :type sort_dir: str
        :param highlight: Enable highlight markers
        :type highlight: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('search.all',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': str(highlight).lower(),
                            'count': count,
                            'page': page
                        })

    def files(self, query, sort=None, sort_dir=None, highlight=True,
              count=None, page=None):
        """
        Searches for files matching a query

        :param query: Search query
        :type query: str
        :param sort: Sort by score or timestamp
        :type sort: str
        :param sort_dir: Sort direction asc or desc
        :type sort_dir: str
        :param highlight: Enable highlight markers
        :type highlight: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('search.files',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': str(highlight).lower(),
                            'count': count,
                            'page': page
                        })

    def messages(self, query, sort=None, sort_dir=None, highlight=True,
                 count=None, page=None):
        """
        Searches for messages matching a query

        :param query: Search query
        :type query: str
        :param sort: Sort by score or timestamp
        :type sort: str
        :param sort_dir: Sort direction asc or desc
        :type sort_dir: str
        :param highlight: Enable highlight markers
        :type highlight: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('search.messages',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': str(highlight).lower(),
                            'count': count,
                            'page': page
                        })
