========
Slackest
========

About
=====

Slackest is a full-featured Python interface for the `Slack API
<https://api.slack.com/>`_.

Examples
========
.. code-block:: python

    from slackest import Slackest

    slack = Slackest('<your-slack-api-token-goes-here>')

    # Send a message to #general channel
    slack.chat.post_message('#general', 'Hello fellow slackers!')

    # Get users list
    response = slack.users.list()
    users = response.body['members']

    # Upload a file
    slack.files.upload('hello.txt')

    # If you need to proxy the requests
    proxy_endpoint = 'http://myproxy:3128'
    slack = Slackest('<your-slack-api-token-goes-here>',
                    http_proxy=proxy_endpoint,
                    https_proxy=proxy_endpoint)

    # Advanced: Use `request.Session` for connection pooling (reuse)
    from requests.sessions import Session
    with Session() as session:
        slack = Slacker(token, session=session)
        slack.chat.post_message('#general', 'All these requests')
        slack.chat.post_message('#general', 'go through')
        slack.chat.post_message('#general', 'a single https connection')

Installation
============

.. code-block:: bash

    $ pip install git+https://github.com/Cox-Automotive/slackest

Documentation
=============

https://api.slack.com/methods

TODO
====

* ~~Convenience functions within the main Slackest class~~
* Test completion
* CICD
* Publish to PyPi
