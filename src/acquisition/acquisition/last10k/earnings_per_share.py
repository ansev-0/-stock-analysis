from src.acquisition.acquisition.last10k.last10k import Last10K

class EarningsPerShare(Last10K):
    @Last10K._get_data
    def get(self, form_type, filing_order):
        return 'earningspershare', {'formType' : form_type, 'filingOrder' : filing_order}