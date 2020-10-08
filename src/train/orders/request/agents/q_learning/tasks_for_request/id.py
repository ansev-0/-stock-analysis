from datetime import datetime

class IdTask:
    def __call__(self):
        return datetime.now()
