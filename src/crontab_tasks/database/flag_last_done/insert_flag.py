from src.crontab_tasks.database.flag_last_done.database import FlagsLastDoneCronTab


class InsertFlagLastDoneCronTab(FlagsLastDoneCronTab):

    def insert_one(self, dict_to_insert, **kwargs):
        return self.collection.insert_one(dict_to_insert, **kwargs)

    def insert_many(self, list_dict_to_insert, **kwargs):
        return self.collection.insert_many(list_dict_to_insert, **kwargs)
        