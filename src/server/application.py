from flask import Flask, request
from flask_restplus import Api
from src.config.server import environment_config


class Application(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app,
                       version='1.0',
                       title='News Portal API',
                       description='News Portal API',
                       doc=environment_config["swagger-url"]
                       )
        self.req = request

    def run(self):
        self.app.run(
            debug=environment_config["debug"],
            port=environment_config["port"]
        )


server = Application()
