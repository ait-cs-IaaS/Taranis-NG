from flask_restful import Api

from api import *


def initialize(app):
    api = Api(app)

    isalive.initialize(api)
    presenters.initialize(api)
