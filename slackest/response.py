import json

class Response(object):
    """Requests response object"""

    def __init__(self, body):
        self.raw = body
        self.body = json.loads(body)
        self.successful = self.body['ok']
        self.error = self.body.get('error')

    def __str__(self):
        return json.dumps(self.body)