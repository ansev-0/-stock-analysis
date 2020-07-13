import pandas as pd
import matplotlib.pyplot as plt

def show_predictions_by_days(df_comp):
    
    for date, group in  df_comp.groupby(pd.Grouper(freq='D')):
        date = date.strftime('%Y-%m-%d')
        print(f'Date : {date}')
        diff = group['test'].sub(group['real'])
        mean = (diff) / 2
        str_error = diff.round(1).astype(str)
        
        fig=group.plot(figsize=(22, 12), linewidth=3, grid=True, style=['o-', 'g<'])
        plt.errorbar(group.index, group['real'] + mean, 
                     yerr= mean,
                 label='error', fmt='g.', ecolor='green', elinewidth=2)
    
        for i in group.index:
            plt.text(i, 
                     group.loc[i, 'real'] + mean[i],
                     s = str_error.loc[i], 
                     fontsize=15)
            
        plt.fill_between(group.index, group['real'], group['test'],
                         color='green', alpha='0.05')

        fig.legend(fontsize=20)
        plt.yticks(size=15)
        plt.show(block=False)
