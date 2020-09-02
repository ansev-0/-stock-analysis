from nolitsa.dimension import fnn
import numpy as np
import pandas as pd
import nolds
import matplotlib.pyplot as plt


def test_ar(x, k, return_vr=False):
    
    #if the series corresponds to the random path,
    #then the test result approximates a normal distribution.

    # Reference
    # https://www.redalyc.org/pdf/818/81835367006.pdf
    
    T = len(x) 
    r = x.diff() 
    mu = r.mean()  
    r_diff_mu = r.sub(mu).pow(2) 
    
    #calculate var_1
    var_1 = r_diff_mu.mean() 
    alpha_den = r_diff_mu.sum() ** 2
    C = 1 / (k * (T - k + 1) * (1 - k/T))
    
    #calculate var_K
    var_k =  C * x[k:].sub(x.shift(k)[k:]).sub(k * mu).pow(2).sum() 
    vr = var_k / var_1 
    
    #take into account heteroscedasticity
    coef = (np.arange(start=k-1, stop=0, step=-1) * 2 / k) ** 2
    alpha = np.array([r.shift(j).sub(mu).pow(2).mul(r_diff_mu).sum() 
                      for j in range(1, k)]) / alpha_den
    teta = np.sum(alpha * coef) 
    result = (vr - 1) / (teta ** 0.5) 
    
    #output
    if return_vr:
        return vr, result
    
    return result


def best_embed(serie, range_fnn, min_fnn=0.05, ra_fnn=5, debug_plot=False, return_df=False, return_min_fnn=False):
    output = []
    #calculate sampen
    sampen_values = [nolds.sampen(serie, val) for val in range_fnn]

    #calculate fnn
    fnn_result = fnn(serie, dim = range_fnn, window=1, scale_d=True)
    df = pd.DataFrame(data=fnn_result.T, 
                      columns=['Test1', 'Test2', 'Total'], 
                      index=range_fnn).assign(sampen=sampen_values)

    
    lt_min_fnn = df['Total'].lt(min_fnn)
    mask_fnn = lt_min_fnn & df['Total'].le(df['Total'].min() * ra_fnn)
    df_mask_fnn = df.loc[mask_fnn]
    optimal = df_mask_fnn['sampen'].idxmin()
    output.append(optimal)

    #debug plot
    if debug_plot:
        
        df.plot()
        plt.plot(df['sampen'], '^', markersize=10,
                 color='g', label = 'optimal',
                 markevery = [optimal - df.index[0]])
        
        plt.grid()
        
        df_mask_fnn.plot()

        plt.plot(df_mask_fnn['sampen'], '^', markersize=10, 
                 color='g', label = 'optimal', 
                 markevery = [optimal - df_mask_fnn.index[0]])
        plt.grid()
    
    if return_df:
        output.append(df)

    if return_min_fnn:
        output.append(lt_min_fnn.idxmax())
    
    return  tuple(output)


def hurst_rolling(data, m):
    return np.abs(data.rolling(m).apply(nolds.hurst_rs).mean()-0.5)
    
    