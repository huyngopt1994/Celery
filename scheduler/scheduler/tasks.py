from celery import Celery, Task
import time

import os
class AddTask(Task):
    name = "add"

    def run(self, a, b):
        return a + b


# Create app
app = Celery('tasks', broker='amqp://guest@localhost')
app.register_task(AddTask())

app.conf.beat_schedule = {
    'add': {
        'task': 'add',
        'schedule': 5,
        'args': [
            4, 4
        ]
    }
}
