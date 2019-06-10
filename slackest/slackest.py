from .slackest_error import SlackestError
from .response import Response
from .base_api import BaseAPI
from .api import API
from .auth import Auth
from .dialog import Dialog
from .users_profile import UsersProfile
from .users_admin import UsersAdmin
from .users import Users
from .groups import Groups
from .channels import Channels
from .conversation import Conversation
from .chat import Chat
from .im import IM
from .mpim import MPIM
from .search import Search
from .files_comments import FilesComments
from .files import Files
from .stars import Stars
from .emoji import Emoji
from .presence import Presence
from .rtm import RTM
from .team_profile import TeamProfile
from .team import Team
from .pins import Pins
from .user_group_users import UserGroupsUsers
from .user_groups import UserGroups
from .dnd import DND
from .reminders import Reminders
from .bots import Bots
from .idp_groups import IDPGroups
from .oauth import OAuth
from .apps_permissions import AppsPermissions
from .apps import Apps
from .incoming_webhook import IncomingWebhook
from .reactions import Reactions
from .constants import DEFAULT_TIMEOUT, DEFAULT_RETRIES 

class Slackest(object):
    """The main Slackest work horse. Surfaces some convenience methods but mostly
    interfaces with the auxilary classes."""

    oauth = OAuth(timeout=DEFAULT_TIMEOUT)

    def __init__(self, token, incoming_webhook_url=None,
                 timeout=DEFAULT_TIMEOUT, http_proxy=None, https_proxy=None,
                 session=None, rate_limit_retries=DEFAULT_RETRIES):

        proxies = self.__create_proxies(http_proxy, https_proxy)
        api_args = {
            'token': token,
            'timeout': timeout,
            'proxies': proxies,
            'session': session,
            'rate_limit_retries': rate_limit_retries,
        }
        self.im = IM(**api_args)
        self.api = API(**api_args)
        self.dnd = DND(**api_args)
        self.rtm = RTM(**api_args)
        self.apps = Apps(**api_args)
        self.auth = Auth(**api_args)
        self.bots = Bots(**api_args)
        self.conversation = Conversation(**api_args)
        self.chat = Chat(**api_args)
        self.dialog = Dialog(**api_args)
        self.team = Team(**api_args)
        self.pins = Pins(**api_args)
        self.mpim = MPIM(**api_args)
        self.users = Users(**api_args)
        self.files = Files(**api_args)
        self.stars = Stars(**api_args)
        self.emoji = Emoji(**api_args)
        self.search = Search(**api_args)
        self.groups = Groups(**api_args)
        self.channels = Channels(**api_args)
        self.presence = Presence(**api_args)
        self.reminders = Reminders(**api_args)
        self.reactions = Reactions(**api_args)
        self.idpgroups = IDPGroups(**api_args)
        self.usergroups = UserGroups(**api_args)
        self.incomingwebhook = IncomingWebhook(url=incoming_webhook_url,
                                               timeout=timeout, proxies=proxies)

    def __create_proxies(self, http_proxy=None, https_proxy=None):
        """
        Creates the appropriate proxy type

        :param http_proxy: An HTTP proxy
        :type http_proxy: bool
        :param https_proxy: An HTTPS proxy
        :type https_proxy: bool
        :return: A dictionary of proxy configurations
        :rtype: dict
        """
        proxies = dict()
        if http_proxy:
            proxies['http'] = http_proxy
        if https_proxy:
            proxies['https'] = https_proxy
        return proxies

    def create_channel(self, name, is_private=True, users=[]):
        """
        Creates a channel

        :param name: The channel name
        :type name: str
        :param is_private: Determines if channel is private (like a group)
        :type is_private: bool
        :param user_ids: A list of User IDs to add to the channel
        :type user_ids: list[str]
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.create(name, is_private, users)

    def get_channels(self, exclude_archive, types):
        """
        Lists all channels

        :param exclude_archived: Exclude archived channels
        :type exclude_archived: bool
        :param types: The type of channel to return, can be one of public_channel, private_channel
        :type types: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.list_all(exclude_archived=exclude_archive, types=types)

    def list_all_users(self):
        """
        Lists all users

        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.users.list_all(include_locale=True)

    def kick_user(self, channel, user):
        """
        Removes a user from a channel

        :param channel: The channel ID
        :type channel: str
        :param user: The user ID
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.kick(channel, user)

    def history_all(self, channel):
        """
        Fetches all history of messages and events from a channel

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.history_all(channel)

    def post_message_to_channel(self, channel, message):
        """
        Posts a message to a channel

        :param channel: The channel ID
        :type channel: str
        :param message: The message text
        :type message: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.chat.post_message(channel, text=message, link_names=True)

    def post_thread_to_message(self, channel, message, thread_ts):
        """

        :param channel: The channel ID
        :type channel: str
        :param message: The message text
        :type message: str
        :param thread_ts: The parent thread timestamp identifier
        :type thread_ts: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.chat.post_message(channel, text=message, thread_ts=thread_ts, link_names=True)

    def add_member_to_channel(self, channel, member):
        """
        Invites a user to a channel

        :param channel: The channel ID
        :type channel: str
        :param user: A user ID to invite to a channel
        :type user: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.invite(channel, member)

    def get_channel_info(self, channel):
        """
        Gets information about a channel.

        :param channel: The channel ID
        :type channel: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.channels.info(channel)

    def get_replies(self, channel, time_stamp):
        """
        Fetches all replies in a thread of messages

        :param channel: The channel ID
        :type channel: str
        :param time_stamp: Unique identifier of a thread's parent message
        :type time_stamp: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.replies_all(channel, time_stamp)

    def set_purpose(self, channel, purpose):
        """
        Sets the purpose a channel

        :param channel: The channel ID
        :type channel: str
        :param purpose: The purpose to set
        :type purpose: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.setPurpose(channel, purpose)

    def set_topic(self, channel, topic):
        """
        Sets the topic a channel

        :param channel: The channel ID
        :type channel: str
        :param topic: The topic to set
        :type topic: str
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.conversation.setTopic(channel, topic)

    def upload_file(self, filename, channels):
        """
        Uploads a file to a channel

        :param filename: The filename to upload
        :type filename: str
        :param channels: Channel IDs to upload to
        :type channels: list[str]
        :return: A response object to run the API request.
        :rtype: :class:`Response <Response>` object
        """
        return self.files.upload(filename, channels=channels)
