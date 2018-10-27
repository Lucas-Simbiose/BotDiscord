from ..base import BaseMongo
from ...utils import error_messages

class Workers(BaseMongo):
    db_string = "worker"
    collection_strings = ["queue_workers"]

    def create_worker(self, user_):
        user = self.workers.find_one({'_id': user_.id})
        if user:
            return {
                'status': 'error',
                'code': 3000
            }
        new_user = {
            "_id": user_.id,
            "username": user_.name,
        }
        self.workers.insert_one(new_user)
        return {"status": "success", "msg": "User {} has been successfully registered!"}