========
Slackest
========

|build status|
|pylint|

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
        slack = Slackest(token, session=session)
        slack.chat.post_message('#general', 'All these requests')
        slack.chat.post_message('#general', 'go through')
        slack.chat.post_message('#general', 'a single https connection')

Installation
============

.. code-block:: bash

    $ pip install slackest

CICD
====

This project uses AWS CodeBuild to build. CodeBuild uses a YAML-based file called builspec.yml that runs the appropriate commands.

A wheel and a source distribution is provided according to the buildspec.

Building Locally
----------------

For local build testing, use the local CodeBuild image. See `this AWS blog post <https://aws.amazon.com/blogs/devops/announcing-local-build-support-for-aws-codebuild/>`_ for more details.

.. code-block:: bash

    $ git clone https://github.com/aws/aws-codebuild-docker-images.git
    $ cd aws-codebuild-docker-images/ubuntu/python/3.7.1
    $ docker build -t aws/codebuild/python:3.7.1 .
    $ docker pull amazon/aws-codebuild-local:latest --disable-content-trust=false
    $ wget https://raw.githubusercontent.com/aws/aws-codebuild-docker-images/master/local_builds/codebuild_build.sh && chmod +x codebuild_build.sh
    $ ./codebuild_build.sh -i aws/codebuild/python:3.7.1 -a /tmp/codebuild/


Documentation
=============

Slack API
---------

https://api.slack.com/methods

Slackest
--------

https://s3.amazonaws.com/slackest/index.html

TODO
====

* Test completion, full coverage


.. |build status| image:: https://codebuild.us-east-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoibStlNTVWVjBDMk1hOFU4ekRiNlNRdExXeCtSZFFsdlN0UjRnZzJsU2VNaDBqc3IwRnlmM2lSVG1zcjh2NEZ0WVoyQ0hwVStxU3VoblRIc2NxVjRYRU5vPSIsIml2UGFyYW1ldGVyU3BlYyI6Im5NSjdaT1lFM2hKaWxiR1IiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master
.. |pylint| image:: https://slackest.s3.amazonaws.com/pylint.svg?token=_asjdn22adon2
