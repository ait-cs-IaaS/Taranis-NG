from celery import Celery
from flask import Flask
from celery.bin import worker


class QueueManager:
    def __init__(self, app: Flask):
        self.celery = self.init_app(app)

    def init_app(self, app: Flask):
        celery_app = Celery(app.name)
        celery_app.config_from_object(app.config["CELERY"])
        celery_app.set_default()
        app.extensions["celery"] = celery_app
        return celery_app
