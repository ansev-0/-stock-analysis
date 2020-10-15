import numpy as np

def risk_by_transaction_size(reward, frac=None, tau_n=0.01, tau_frac=1, n_stocks=None, p_n_stocks=0.5, p_frac=0.5,  *args, **kwargs):

    r_nstocks_i = 1
    r_n_stocks_f = 0.2
    r_frac_i = 1
    r_frac_f = 0.2
    r_nstocks = r_n_stocks_f + (r_nstocks_i - r_n_stocks_f) / np.exp(n_stocks * tau_n)
    r_frac = r_frac_f + (r_frac_i - r_frac_f) / np.exp(frac * tau_frac)
    r = (p_n_stocks * r_nstocks) + (p_frac * r_frac)
    return reward * r if reward >= 0 else reward * (2-r)
