#!/usr/bin/python
# -*- coding: utf-8 -*-

good_conversation_list_response = {
    "ok": "true",
    "channels": [
        { 
            "id": "G0AKFJBEU", "name": "mpdm-mr.banks--slactions-jackson--beforebot-1",
            "is_channel": "false", "is_group": "true", "is_im": "false", "created": 1493657761,
            "creator": "U061F7AUR", "is_archived": "false", "is_general": "false", "unlinked": 0,
            "name_normalized": "mpdm-mr.banks--slactions-jackson--beforebot-1", "is_shared": "false",
            "is_ext_shared": "false", "is_org_shared": "false", "pending_shared": [],
            "is_pending_ext_shared": "false", "is_member": "true", "is_private": "true", "is_mpim": "true",
            "is_open": "true", "topic": { "value": "Group messaging", "creator": "U061F7AUR",
            "last_set": 1493657761 }, "purpose": {
            "value": "Group messaging with: @mr.banks @slactions-jackson @beforebot",
            "creator": "U061F7AUR", "last_set": 1493657761 }, "priority": 0
        },
        {
            "id": "D0C0F7S8Y", "created": 1498500348, "is_im": "true", "is_org_shared": "false",
            "user": "U0BS9U4SV", "is_user_deleted": "false", "priority": 0
        },
        {
            "id": "D0BSHH4AD", "created": 1498511030, "is_im": "true", "is_org_shared": "false",
            "user": "U0C0NS9HN", "is_user_deleted": "false", "priority": 0
        }
    ],
    "response_metadata": { }
}

bad_conversation_list_response = {
    "ok": "false", "error": "invalid_auth"
}

good_kick_user_response = { "ok": 'true' }

bad_kick_user_response = { "ok": 'false', "error": 'user_not_found' }

good_channel_list_response = {
    "ok": "true",
    "channels": [
        {
            "id": "C0G9QF9GW", "name": "random", "is_channel": "true",
            "created": 1449709280, "creator": "U0G9QF9C6", "is_archived": "false",
            "is_general": "false", "name_normalized": "random", "is_shared": "false",
            "is_org_shared": "false", "is_member": "true", "is_private": "false",
            "is_mpim": "false", "members": [ "U0G9QF9C6", "U0G9WFXNZ" ],
            "topic": { "value": "Other stuff", "creator": "U0G9QF9C6",
            "last_set": 1449709352 }, "purpose": {
            "value": "A place for non-work-related flimflam, faffing, hodge-podge or jibber-jabber you'd prefer to keep out of more focused work-related channels.",
            "creator": "", "last_set": 0 }, "previous_names": [], "num_members": 2
        },
        {
            "id": "C0G9QKBBL", "name": "general", "is_channel": "true", "created": 1449709280,
            "creator": "U0G9QF9C6", "is_archived": "false", "is_general": "true",
            "name_normalized": "general", "is_shared": "false", "is_org_shared": "false",
            "is_member": "true", "is_private": "false", "is_mpim": "false",
            "members": [ "U0G9QF9C6", "U0G9WFXNZ" ], "topic": { "value": "Talk about anything!",
            "creator": "U0G9QF9C6", "last_set": 1449709364 }, "purpose": {
            "value": "To talk about anything!", "creator": "U0G9QF9C6", "last_set": 1449709334 },
            "previous_names": [], "num_members": 2
        }
    ],
    "response_metadata": { "next_cursor": "dGVhbTpDMUg5UkVTR0w=" }
}

bad_channel_list_response = { "ok": "false", "error": "invalid_auth" }

good_channel_info_response = {
    "ok": "true",
    "channel": {
        "id": "C1H9RESGL", "name": "busting", "is_channel": "true",
        "created": 1466025154, "creator": "U0G9QF9C6", "is_archived": "false",
        "is_general": "false", "name_normalized": "busting", "is_shared": "false",
        "is_org_shared": "false", "is_member": "true", "is_private": "false",
        "is_mpim": "false", "last_read": "1503435939.000101", "latest": {
        "text": "Containment unit is 98% full", "username": "ecto1138",
        "bot_id": "B19LU7CSY", "attachments": [ { "text": "Don't get too attached",
        "id": 1, "fallback": "This is an attachment fallback" } ], "type": "message",
        "subtype": "bot_message", "ts": "1503435956.000247" }, "unread_count": 1,
        "unread_count_display": 1, "members": [ "U0G9QF9C6", "U1QNSQB9U" ],
        "topic": { "value": "Spiritual containment strategies", "creator": "U0G9QF9C6",
        "last_set": 1503435128 }, "purpose": { "value": "Discuss busting ghosts",
        "creator": "U0G9QF9C6", "last_set": 1503435128 },
        "previous_names": [ "dusting" ] 
    }
} 

bad_channel_info_response = { "ok": 'false', "error": "channel_not_found" }

good_user_list_response = {
    "ok": "true",
    "members": [
        {
            "id": "W012A3CDE", "team_id": "T012AB3C4", "name": "spengler",
            "deleted": "false", "color": "9f69e7", "real_name": "spengler",
            "tz": "America/Los_Angeles", "tz_label": "Pacific Daylight Time",
            "tz_offset": -25200, "profile": { "avatar_hash": "ge3b51ca72de",
            "status_text": "Print is dead", "status_emoji": ":books:",
            "real_name": "Egon Spengler", "display_name": "spengler",
            "real_name_normalized": "Egon Spengler", "display_name_normalized": "spengler",
            "email": "spengler@ghostbusters.example.com", "image_24": "https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg",
            "image_32": "https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg", "image_48": "https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg",
            "image_72": "https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg", "image_192": "https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg",
            "image_512": "https://.../avatar/e3b51ca72dee4ef87916ae2b9240df50.jpg", "team": "T012AB3C4" },
            "is_admin": "true", "is_owner": "false", "is_primary_owner": "false",
            "is_restricted": "false", "is_ultra_restricted": "false", "is_bot": "false",
            "updated": 1502138686, "is_app_user": "false", "has_2fa": "false"
        },
        {
            "id": "W07QCRPA4", "team_id": "T0G9PQBBK", "name": "glinda",
            "deleted": "false", "color": "9f69e7", "real_name": "Glinda Southgood",
            "tz": "America/Los_Angeles", "tz_label": "Pacific Daylight Time",
            "tz_offset": -25200, "profile": { "avatar_hash": "8fbdd10b41c6",
            "image_24": "https://a.slack-edge.com...png", "image_32": "https://a.slack-edge.com...png",
            "image_48": "https://a.slack-edge.com...png", "image_72": "https://a.slack-edge.com...png",
            "image_192": "https://a.slack-edge.com...png", "image_512": "https://a.slack-edge.com...png",
            "image_1024": "https://a.slack-edge.com...png", "image_original": "https://a.slack-edge.com...png",
            "first_name": "Glinda", "last_name": "Southgood", "title": "Glinda the Good",
            "phone": "", "skype": "", "real_name": "Glinda Southgood",
            "real_name_normalized": "Glinda Southgood", "display_name": "Glinda the Fairly Good",
            "display_name_normalized": "Glinda the Fairly Good",
            "email": "glenda@south.oz.coven" }, "is_admin": "true",
            "is_owner": "false", "is_primary_owner": "false", "is_restricted": "false",
            "is_ultra_restricted": "false", "is_bot": "false", "updated": 1480527098,
            "has_2fa": "false"
        }
    ],
    "cache_ts": 1498777272,
    "response_metadata": { }
} 

bad_user_list_response = {
    "ok": "false", "error": "fatal_error"
}

good_conversation_history_response = {
    "ok": 'true',
    "messages": [
        { "type": "message", "user": "U012AB3CDE",
          "text": "I find you punny and would like to smell your nose letter",
          "ts": "1512085950.000216"
        },
        { "type": "message", "user": "U061F7AUR",
          "text": "What, you want to smell my shoes better?",
          "ts": "1512104434.000490"
        }
    ],
    "has_more": 'false', "pin_count": 0, "response_metadata": { }
} 

bad_conversation_history_response = { "ok": 'false', "error": "channel_not_found" }

good_post_message_to_channel_response = {
    "ok": 'true', "channel": "C1H9RESGL", "ts": "1503435956.000247",
    "message": { 
        "text": "Here's a message for you", "username": "ecto1",
        "bot_id": "B19LU7CSY", "attachments": [ { "text": "This is an attachment",
        "id": 1, "fallback": "This is an attachment's fallback" } ], "type": "message",
        "subtype": "bot_message", "ts": "1503435956.000247"
    }
}

bad_post_message_to_channel_response = { "ok": 'false', "error": "too_many_attachments" }

good_post_thread_to_message_response = {
    "ok": 'true',
    "channel": "C1H9RESGL",
    "ts": "1503435956.000247",
    "message": {
        "text": "Here's a message for you", "username": "ecto1", "bot_id": "B19LU7CSY",
        "attachments": [ { "text": "This is an attachment", "id": 1,
        "fallback": "This is an attachment's fallback" } ], "type": "message",
        "subtype": "bot_message", "ts": "1503435956.000247"
    }
}

bad_post_thread_to_message_response = { "ok": 'false', "error": "is_archived" }

good_add_member_to_channel_response = {
    "ok": 'true',
    "channel": {
        "id": "C012AB3CD", "name": "general", "is_channel": 'true', "is_group": 'false',
        "is_im": 'false', "created": 1449252889, "creator": "W012A3BCD",
        "is_archived": 'false', "is_general": 'true', "unlinked": 0,
        "name_normalized": "general", "is_read_only": 'false', "is_shared": 'false',
        "is_ext_shared": 'false', "is_org_shared": 'false', "pending_shared": [],
        "is_pending_ext_shared": 'false', "is_member": 'true', "is_private": 'false',
        "is_mpim": 'false', "last_read": "1502126650.228446", "topic": {
        "value": "For public discussion of generalities", "creator": "W012A3BCD",
        "last_set": 1449709364 }, "purpose": {
        "value": "This part of the workspace is for fun. Make fun here.", "creator": "W012A3BCD",
        "last_set": 1449709364 }, "previous_names": [ "specifics",
        "abstractions", "etc" ], "num_members": 23, "locale": "en-US"
    }
}

bad_add_member_to_channel_response = { "ok": 'false', "error": "method_not_supported_for_channel_type" }

good_get_replies_reponse = {
    "messages": [
        {
            "type": "message", "user": "U061F7AUR", "text": "island",
            "thread_ts": "1482960137.003543", "reply_count": 3, "replies": [
            { "user": "U061F7AUR", "ts": "1483037603.017503" },
            { "user": "U061F7AUR", "ts": "1483051909.018632" },
            { "user": "U061F7AUR", "ts": "1483125339.020269" }
            ], "subscribed": 'true', "last_read": "1484678597.521003",
            "unread_count": 0, "ts": "1482960137.003543"
        },
        {
            "type": "message", "user": "U061F7AUR", "text": "one island",
            "thread_ts": "1482960137.003543", "parent_user_id": "U061F7AUR",
            "ts": "1483037603.017503"
        },
        {
            "type": "message", "user": "U061F7AUR", "text": "two island",
            "thread_ts": "1482960137.003543", "parent_user_id": "U061F7AUR",
            "ts": "1483051909.018632"
        },
        {
            "type": "message", "user": "U061F7AUR", "text": "three for the land",
            "thread_ts": "1482960137.003543", "parent_user_id": "U061F7AUR",
            "ts": "1483125339.020269"
        }
    ],
    "has_more": 'true', "ok": 'true', "response_metadata": { }
}

bad_get_replies_response = { "ok": 'false', "error": "thread_not_found" }

good_set_purpose_response = { "ok": 'true', "purpose": 'My purpose' }

bad_set_purpose_response = { "ok": 'false', "error": 'too_long' }

good_set_topic_response = { "ok": 'true', "topic": 'My topic' }

bad_set_topic_response = { "ok": 'false', "error": 'user_is_restricted' }

good_upload_file_response = {
    "ok": 'true',
    "file": {
        "id": "F0TD00400", "created": 1532293501, "timestamp": 1532293501,
        "name": "README.rst", "title": "README", "mimetype": "application/text",
        "filetype": "txt", "pretty_type": "TXT", "user": "U0L4B9NSU",
        "editable": 'false', "size": 43518, "mode": "hosted",
        "is_external": 'false', "external_type": "", "is_public": 'false',
        "public_url_shared": 'false', "display_as_bot": 'false', "username": "",
        "url_private": "https://.../readme.rst",
        "url_private_download": "https://.../readme.rst",
        "thumb_64": "https://.../readme_64.rst",
        "thumb_80": "https://.../readme_80.rst",
        "thumb_360": "https://.../readme_360.rst",
        "thumb_360_w": 360, "thumb_360_h": 250,
        "thumb_480": "https://.../readme_480.rst",
        "thumb_480_w": 480, "thumb_480_h": 334,
        "thumb_160": "https://.../readme_160.rst",
        "image_exif_rotation": 1,
        "original_w": 526, "original_h": 366,
        "permalink": "https://.../readme.rst",
        "permalink_public": "https://.../More-Path-Components",
        "comments_count": 0, "is_starred": 'false', "shares": {
        "private": { "D0L4B9P0Q": [ { "reply_users": [], 
        "reply_users_count": 0, "reply_count": 0,
        "ts": "1532293503.000001" } ] } }, "channels": [],
        "groups": [], "ims": [ "D0L4B9P0Q" ], "has_rich_preview": 'false'
    }
}

bad_upload_file_response = { "ok": 'false', "error": "invalid_auth" }
