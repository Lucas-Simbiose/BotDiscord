# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division

import os

from pymongo import MongoClient


class BaseMongo(MongoClient):
    # Set DB
    db_string = "faked_base"
    # Set Collection
    collection_strings = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if os.environ.get("RUNNING_TESTS"):
            self.db_string = "test_" + self.db_string

        self.database = self[self.db_string]
        for collection in self.collection_strings:
            tmp_collection = self.database[collection]
            setattr(self, collection, tmp_collection)
