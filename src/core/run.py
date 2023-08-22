#! /usr/bin/env python

from core import create_app
from gunicorn.arbiter import Arbiter

app = create_app()


def post_worker_init(worker):
    print(worker.pid)


if __name__ == "__main__":
    app.run()
