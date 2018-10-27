# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

from bot import config
from bot.libs.worker.queue_work import QueueWorkers

QUEUE_COLLECTION = QueueWorkers(**config.get("mongo", {}))

def create_queue():
    msg = QUEUE_COLLECTION.create_queue()
    print(msg)
    return

if __name__ == "__main__":
    create_queue()
