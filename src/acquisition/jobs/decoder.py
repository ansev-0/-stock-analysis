from datetime import datetime
from src.tools.importer import importer

class JobsDecoder:
    def __init__(self, job_class):
        self.job_class = job_class

    def __call__(self, job_from_db):
        class_obj = importer(job_from_db['object_class'])
        task_obj = class_obj(*job_from_db['object_args'], 
                             **job_from_db['object_kwargs'])
        return self.job_class(task_obj, job_from_db['apply'])

    @staticmethod
    def _default_dict_status(status):
        return {'status' : status, 'date' : datetime.now()}
    