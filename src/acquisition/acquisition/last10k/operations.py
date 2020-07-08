
from src.acquisition.acquisition.last10k.last10k import Last10K

class Operations(Last10K):
    @Last10K._get_data
    def get(self, form_type, filing_order):
        return 'operations', {'formType' : form_type, 'filingOrder' : filing_order}