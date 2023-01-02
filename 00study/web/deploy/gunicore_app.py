#!/usr/bin/env python3
import gunicorn.app.base


class GunicornApp(gunicorn.app.base.Application):
    """
    Server launcher using the Gunicorn server
    """

    def __init__(self, app, options=dict()):
        self.options = options
        self.application = app
        super(GunicornApp, self).__init__()

    def load_config(self):
        for key, value in self.options.items():
            if key in self.cfg.settings:
                self.cfg.set(key.lower(), value)

    def load(self):
        return self.application
