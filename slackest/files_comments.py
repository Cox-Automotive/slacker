from .base_api import BaseAPI

class FilesComments(BaseAPI):
    """Follows the Slack FilesComments API. See https://api.slack.com/methods"""

    def add(self, file_, comment):
        """
        DEPRECATED - Adds a comment to a file

        :param file_: The file ID
        :type file_: str
        :param comment: Text of the comment
        :type comment: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.comments.add',
                         data={'file': file_, 'comment': comment})

    def delete(self, file_, id):
        """
        Deletes a comment on a file

        :param file_: File to delete a comment from
        :type file_: str
        :param id: The comment ID
        :type id: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.comments.delete',
                         data={'file': file_, 'id': id})

    def edit(self, file_, id, comment):
        """
        DEPRECATED - Edits a comment to a file

        :param file_: File to delete a comment from
        :type file_: str
        :param id: The comment ID
        :type id: str
        :param comment: Text of the comment
        :type comment: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('files.comments.edit',
                         data={'file': file_, 'id': id, 'comment': comment})
