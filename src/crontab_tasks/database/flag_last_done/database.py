from src.crontab_tasks.database.database import DataBaseCronTab

class FlagsLastDoneCronTab(DataBaseCronTab):
    def __init__(self):
        super().__init__('flags_last_done')
