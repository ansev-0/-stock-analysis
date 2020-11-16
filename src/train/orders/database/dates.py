from pandas import to_datetime , Timestamp

class DatetimeDates:

    def dates_for_save(self, **dates):
        return {key : self.to_db(date)
                for key, date in dates.items()}

    def dates_for_update(self, **dates):
        return {'$set' : self.dates_for_save(**dates)}

    def dates_for_save_from_tuples(self, keys, values):

        return dict(zip(keys, 
                        map(self.to_db, values)
                        )
        )
    @staticmethod
    def to_db(date):
        if isinstance(date, Timestamp):
            return date
        elif isinstance(date, str):
            return to_datetime(date)
            
        raise ValueError('You must pass a instance of Timestamp or str')
