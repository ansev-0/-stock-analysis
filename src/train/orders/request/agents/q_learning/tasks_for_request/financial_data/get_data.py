from src.read_database.financial_data.reader_many_financial_features import ManyFinancialFeaturesFromDataBase
from pandas.tseries.offsets import DateOffset
from src.train.orders.request.agents.q_learning.tasks_for_request.transform_data import TransformData
import pandas as pd
import numpy as np

class GetDataTask:
    _transform_data = TransformData(4)
    _features =['cash_flow_capitalExpenditures',
                'cash_flow_cashflowFromFinancing',
                'cash_flow_cashflowFromInvestment',
                'cash_flow_changeInCashAndCashEquivalents',
                'cash_flow_changeInExchangeRate',
                'cash_flow_changeInOperatingAssets',
                'cash_flow_changeInOperatingLiabilities',
                'cash_flow_changeInReceivables',
                'cash_flow_depreciationDepletionAndAmortization',
                'cash_flow_netIncome',
                'cash_flow_operatingCashflow',
                'cash_flow_paymentsForOperatingActivities',
                'cash_flow_paymentsForRepurchaseOfCommonStock',
                'cash_flow_paymentsForRepurchaseOfEquity',
                'cash_flow_proceedsFromRepurchaseOfEquity',
                'cash_flow_profitLoss',
                'earnings_estimatedEPS',
                'earnings_reportedEPS',
                'earnings_surprise',
                'earnings_surprisePercentage',
                'balance_sheet_capitalLeaseObligations',
                'balance_sheet_cashAndCashEquivalentsAtCarryingValue',
                'balance_sheet_cashAndShortTermInvestments',
                'balance_sheet_commonStock',
                'balance_sheet_commonStockSharesOutstanding',
                'balance_sheet_currentAccountsPayable',
                'balance_sheet_currentDebt',
                'balance_sheet_currentLongTermDebt',
                'balance_sheet_currentNetReceivables',
                'balance_sheet_deferredRevenue',
                'balance_sheet_goodwill',
                'balance_sheet_intangibleAssets',
                'balance_sheet_intangibleAssetsExcludingGoodwill',
                'balance_sheet_inventory',
                'balance_sheet_investments',
                'balance_sheet_longTermDebt',
                'balance_sheet_longTermDebtNoncurrent',
                'balance_sheet_longTermInvestments',
                'balance_sheet_otherCurrentAssets',
                'balance_sheet_otherCurrentLiabilities',
                'balance_sheet_otherNonCurrentLiabilities',
                'balance_sheet_otherNonCurrrentAssets',
                'balance_sheet_propertyPlantEquipment',
                'balance_sheet_retainedEarnings',
                'balance_sheet_shortLongTermDebtTotal',
                'balance_sheet_shortTermDebt',
                'balance_sheet_shortTermInvestments',
                'balance_sheet_totalAssets',
                'balance_sheet_totalCurrentAssets',
                'balance_sheet_totalCurrentLiabilities',
                'balance_sheet_totalLiabilities',
                'balance_sheet_totalNonCurrentAssets',
                'balance_sheet_totalNonCurrentLiabilities',
                'balance_sheet_totalShareholderEquity',
                'income_statement_comprehensiveIncomeNetOfTax',
                'income_statement_costOfRevenue',
                'income_statement_costofGoodsAndServicesSold',
                'income_statement_depreciationAndAmortization',
                'income_statement_ebit',
                'income_statement_ebitda',
                'income_statement_grossProfit',
                'income_statement_incomeBeforeTax',
                'income_statement_incomeTaxExpense',
                'income_statement_interestAndDebtExpense',
                'income_statement_interestExpense',
                'income_statement_interestIncome',
                'income_statement_netIncome',
                'income_statement_netIncomeFromContinuingOperations',
                'income_statement_netInterestIncome',
                'income_statement_nonInterestIncome',
                'income_statement_operatingExpenses',
                'income_statement_operatingIncome',
                'income_statement_otherNonOperatingIncome',
                'income_statement_researchAndDevelopment',
                'income_statement_sellingGeneralAndAdministrative',
                'income_statement_totalRevenue']

    _reader = ManyFinancialFeaturesFromDataBase()

    def __call__(self, symbol, index):

        #index_init = index.copy()
        financial_data = self._prepare_data(
            self._make_request_db(symbol, index)
        )
        self._check_index(financial_data[1], index)

        return financial_data

        
    def _make_request_db(self, symbol, index):
        return self._reader.get(symbol, 
                                *self._get_limits_from_index(index))
   
    @staticmethod
    def _get_limits_from_index(index):
        i1, i2 = tuple(index[[0,-1]])
        i1 = i1 - DateOffset(years=2)
        return i1, i2
        
    @staticmethod
    def _check_index(financial_index, index_init):
       if financial_index[0] > index_init[0]:
            index_0 = index_init[0]
            raise ValueError (f'No financial data in {index_0}') 

    
    def _prepare_data(self, data):
        numeric_df = data.loc[:, self._features].apply(lambda x: pd.to_numeric(x , errors='coerce')).fillna(0)
        
        m = numeric_df.lt(0)
        numeric_df = np.log1p(numeric_df.abs())
        numeric_df = numeric_df.mask(m, -numeric_df).fillna(0)
        sequences = self._transform_data.get_sequences(numeric_df)
        return sequences, numeric_df.index[5:], numeric_df.columns
        
        

        





