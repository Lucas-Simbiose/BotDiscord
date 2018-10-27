# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division
from datetime import datetime

from ..base import BaseMongo
from ...utils import error_messages
from .workers import Workers

class QueueWorkers(BaseMongo):
    db_string = "worker"
    collection_strings = ["queue_workers"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workers_instance = Workers(*args, **kwargs)

    def create_queue(self):
        queue = self.queue_workers.find_one({"_id": "work_queue"})
        if queue:
            return "Queue already created."
        self.queue_workers.insert_one({"_id": "work_queue", "workers": []})
        return "Queue successfully created."

    def add_worker(self, user_id):
        worker = self.workers_instance.get_user(user_id)
        if not worker:
            return {
                'status': 'error',
                'code': 3001
            }
        queue = self.queue_workers.find_one({"_id": "work_queue"})
        if not queue:
            return {
                'status': 'error',
                'code': 3002
            }
        workers_list = queue['workers']
        for item in workers_list:
            if item['_id'] == user_id:
                return {
                    'status': 'error',
                    'code': 3003
                }
        time = datetime.now()
        user = self.workers_instance.get_user(user_id)
        data = {
            '_id': user_id,
            'name': user['username'],
            'entry': time
        }
        workers_list.append(data)
        self.queue_workers.update_one({"_id": "work_queue"},{"$set": {"workers": workers_list}})
        return {'status': 'success', 'msg': "Welcome to work {}!"}

    def remove_worker(self, user_id):
        worker = self.workers_instance.get_user(user_id)
        if not worker:
            return {
                'status': 'error',
                'code': 3001
            }
        queue = self.queue_workers.find_one({"_id": "work_queue"})
        if not queue:
            return {
                'status': 'error',
                'code': 3002
            }
        workers_list = queue['workers']
        should_remove = False
        user_to_remove = ""
        for item in workers_list:
            if item['_id'] == user_id:
                should_remove = True
                user_to_remove = item
                break
        if not should_remove:
            return {
                'status': 'error',
                'code': 3004
            }
        workers_list.remove(user_to_remove)
        self.queue_workers.update_one({"_id": "work_queue"}, {"$set": {"workers": workers_list}})
        return {'status': 'success', 'msg': "See you tomorrow {}!"}

    def check_active_workers(self):
        queue = self.queue_workers.find_one({"_id": "work_queue"})
        if not queue:
            return {
                'status': 'error',
                'code': 3002
            }
        workers_list = queue['workers']
        total_users = len(workers_list)
        if total_users == 0:
            return {
                'status': 'error',
                'code': 3005
            }
        msg = 'There are currently ' + str(total_users) + ' workers online!\n'

        for user in workers_list:
            prepare_message = user['name'] + ' - arrived at: ' + str(user['entry'].strftime("%Y-%m-%d %H:%M:%S")) +'\n'
            msg += prepare_message
        return {'status': 'success', 'msg': msg}
