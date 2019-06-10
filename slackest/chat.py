import json
from .base_api import BaseAPI

class Chat(BaseAPI):
    """Follows the Slack Chat API. See https://api.slack.com/methods"""

    def post_message(self, channel, text=None, username=None, as_user=False,
                     parse=None, link_names=None, attachments=None,
                     unfurl_links=None, unfurl_media=None, icon_url=None,
                     icon_emoji=None, thread_ts=None, reply_broadcast=None):
        """
        Posts a message to a channel

        :param channel: The channel ID
        :type channel: str
        :param text: Text of the message to post
        :type text: str
        :param username: The username to post as, must be used w/ as_user
        :type username: str
        :param as_user: Posts as the user instead of a bot
        :type as_user: bool
        :param parse: Change how messages are treated
        :type parse: str
        :param link_names: Find and link channel names and username
        :type link_names: str
        :param attachments: JSON based array of structured attachments
        :type attachments: JSON
        :param unfurl_links: Enable unfurling of links
        :type unfurl_links: str
        :param unfurl_media: Enable unfurling of media
        :type unfurl_media: str
        :param icon_url: The icon URL
        :type icon_url: str
        :param icon_emoji: Emoji to use as the icon for this message
        :type icon_emoji: str
        :param thread_ts: Provide another messages ts value to make this message a reply
        :type thread_ts: str
        :param reply_broadcast: Indicates whether reply should be visible in the channel
        :type reply_broadcast: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # Ensure attachments are json encoded
        if attachments:
            if isinstance(attachments, list):
                attachments = json.dumps(attachments)

        return self.post('chat.postMessage',
                         data={
                             'channel': channel,
                             'text': text,
                             'username': username,
                             'as_user': str(as_user).lower(),
                             'parse': parse,
                             'link_names': link_names,
                             'attachments': attachments,
                             'unfurl_links': unfurl_links,
                             'unfurl_media': unfurl_media,
                             'icon_url': icon_url,
                             'icon_emoji': icon_emoji,
                             'thread_ts': thread_ts,
                             'reply_broadcast': reply_broadcast
                         })

    def me_message(self, channel, text):
        """
        Share a me message to a channel

        :param channel: The channel to post to
        :type channel: str
        :param text: The text of the message
        :type text: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('chat.meMessage',
                         data={'channel': channel, 'text': text})

    def command(self, channel, command, text):
        """
        DEPRECATED? Run a command in a chat

        :param channel: The channel ID
        :type channel: str
        :param command: The command to run
        :type command: str
        :param text: The text attached to the command
        :type text: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('chat.command',
                         data={
                             'channel': channel,
                             'command': command,
                             'text': text
                         })

    def update(self, channel, time_stamp, text, attachments=None, parse=None,
               link_names=None, as_user=False):
        """
        Updates a message in a channel

        :param channel: The channel ID
        :type channel: str
        :param time_stamp: Timestamp of the message to be updated
        :type time_stamp: str
        :param text: New text for the message
        :type text: str
        :param attachments: JSON array of structured attachments
        :type attachments: JSON
        :param parse: Change hor messages are treated
        :type parse: str
        :param link_names: Find and link channel names
        :type link_names: str
        :param as_user: Update the message as the authed user
        :type as_user: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # Ensure attachments are json encoded
        if attachments is not None and isinstance(attachments, list):
            attachments = json.dumps(attachments)
        return self.post('chat.update',
                         data={'channel': channel, 'ts': time_stamp, 'text': text,
                               'attachments': attachments, 'parse': parse,
                               'link_names': str(link_names).lower(),
                               'as_user': str(as_user).lower})

    def delete(self, channel, time_stamp, as_user=False):
        """
        Delete a message

        :param channel: The channel ID
        :type channel: str
        :param time_stamp: Timestamp of the message to be deleted
        :type time_stamp: str
        :param as_user: Deletes the message as the authed user
        :type as_user: bool
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('chat.delete',
                         data={'channel': channel, 'ts': time_stamp,
                               'as_user': str(as_user).lower()})

    def post_ephemeral(self, channel, text, user, as_user=False,
                       attachments=None, link_names=True, parse=None):
        """
        Sends an ephemeral message to a user in a channel

        :param channel: The channel ID
        :type channel: str
        :param text: Text of the message to send
        :type text: str
        :param user: The user ID
        :type user: str
        :param as_user: Posts the message as the authed user
        :type as_user: bool
        :param attachments: JSON array of structured attachments
        :type attachments: JSON
        :param link_names: Link channel names and users
        :type link_names: str
        :param parse: Change how messages are treated
        :type parse: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        # Ensure attachments are json encoded
        if attachments is not None and isinstance(attachments, list):
            attachments = json.dumps(attachments)
        return self.post('chat.postEphemeral',
                         data={
                             'channel': channel,
                             'text': text,
                             'user': user,
                             'as_user': str(as_user).lower(),
                             'attachments': attachments,
                             'link_names': str(link_names).lower(),
                             'parse': str(parse).lower(),
                         })

    def unfurl(self, channel, time_stamp, unfurls, user_auth_message=None,
               user_auth_required=False, user_auth_url=None):
        """
        Provides custom unfurl behavior for user posted URLS

        :param channel: The channel ID
        :type channel: str
        :param time_stamp: Timestamp of the message to add unfurl behavior
        :type time_stamp: str
        :param unfurls: JSON map with keys set to URLS in the message
        :type unfurls: JSON
        :param user_auth_message: Invitation to user to use Slack app
        :type user_auth_message: str
        :param user_auth_required: Slack app required
        :type user_auth_required: bool
        :param user_auth_unfurl: URL for completion
        :type user_auth_unfurl: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.post('chat.unfurl',
                         data={'channel': channel, 'ts': time_stamp,
                               'unfurls': unfurls, 'user_auth_message': user_auth_message,
                               'user_auth_required': int(user_auth_required),
                               'user_auth_url': user_auth_url})

    def get_permalink(self, channel, message_ts):
        """
        Retrieve a permalink URL for a specific extant message

        :param channel:
        :type channel:
        :param message_ts:
        :type message_ts:
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.get('chat.getPermalink',
                        params={'channel': channel, 'message_ts': message_ts})
