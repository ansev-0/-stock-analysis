import pandas as pd

class CheckSplitDataFrameByGroups:
    @staticmethod
    def check_valid_format_output(format_output):
        if format_output not in [list, dict]:
            raise TypeError('Format output must be instance of dict or list')



