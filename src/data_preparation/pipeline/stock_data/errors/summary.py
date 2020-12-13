from src.tools.check_components import check_all_in
from src.exceptions.data_preparation_exceptions import PipelineError
class CheckSummary:
    @staticmethod
    def required_fields(required_fields, summary_fields):
        if not check_all_in(required_fields, summary_fields):
            raise PipelineError(f'Summary must have fields : {required_fields}', ValueError)