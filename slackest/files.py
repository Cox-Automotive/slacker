from .base_api import BaseAPI
from .files_comments import FilesComments

class Files(BaseAPI):
    """Follows the Slack Files API. See https://api.slack.com/methods"""

    def __init__(self, *args, **kwargs):
        super(Files, self).__init__(*args, **kwargs)
        self._comments = FilesComments(*args, **kwargs)

    @property
    def comments(self):
        return self._comments

    def list(self, user=None, ts_from=None, ts_to=None, types=None,
             count=None, page=None, channel=None):
        """
        List of files within a team

        :param user: Filter files to this user ID
        :type user: str
        :param ts_from: Timestamp from = after
        :type ts_from: str
        :param ts_to: Timestamp to = before
        :type ts_to: str
        :param types: Filter files by type
        :type types: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :param channel: Filter files to this channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        yield self.get('files.list',
                        params={
                            'user': user,
                            'ts_from': ts_from,
                            'ts_to': ts_to,
                            'types': types,
                            'count': count,
                            'page': page,
                            'channel': channel
                        })

    def info(self, file_, count=None, page=None, cursor=None, limit=100):
        """
        Gents information about a file

        :param file_: The file ID
        :type file_: str
        :param count: Number of items to return
        :type count: int
        :param page: Page number of results to return
        :type page: int
        :param cursor: The parameter for pagination
        :type cursor: str
        :param limit: Max number of items to return
        :type limit: int
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('files.info',
                        params={'file': file_, 'count': count, 'page': page,
                                'cursor': cursor, 'limit': limit})

    def upload(self, file_=None, content=None, filetype=None, filename=None,
               title=None, initial_comment=None, channels=None, thread_ts=None):
        """
        Uploads or creates a file

        :param file_: The file ID
        :type file_: str
        :param content: File contents via a POST variable
        :type content: binary
        :param filetype: File type identifier
        :type filetype: str
        :param filename: File name
        :type filename: str
        :param title: Title of the file
        :type title: str
        :param initial_comment: Comment on the file
        :type initial_comment: str
        :param channels: CSV of channel names to post to
        :type channels: list[str]
        :param thread_ts: Parent thread to use in a reply
        :type thread_ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        data = {
            'content': content,
            'filetype': filetype,
            'filename': filename,
            'title': title,
            'initial_comment': initial_comment,
            'channels': channels,
            'thread_ts': thread_ts
        }

        if file_:
            if isinstance(file_, str):
                with open(file_, 'rb') as file_name:
                    return self.post('files.upload', data=data, files={'file': file_name})

            return self.post(
                'files.upload', data=data, files={'file': file_}
            )
        else:
            return self.post('files.upload', data=data)

    def delete(self, file_):
        """
        Deletes a file

        :param file_: The file ID
        :type file_: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.delete', data={'file': file_})

    def revoke_public_url(self, file_):
        """
        Revokes public sharing

        :param file_: The file ID
        :type file_: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.revokePublicURL', data={'file': file_})

    def shared_public_url(self, file_):
        """
        Enables public sharing

        :param file_: The file ID
        :type file_: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.sharedPublicURL', data={'file': file_})
