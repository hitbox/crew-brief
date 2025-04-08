from flask import send_file
from flask.views import View

class SendFileView(View):

    def __init__(self, **send_file_kwargs):
        self.send_file_kwargs = send_file_kwargs

    def dispatch_request(self, filename, **kwargs):

        send_kwargs = {
            key: val if not callable(val) else val()
            for key, val in self.send_file_kwargs.items()
        }

        return send_file(filename, **send_kwargs)
