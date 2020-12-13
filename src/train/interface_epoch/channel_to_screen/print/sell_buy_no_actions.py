
class SellBuyNoActionsOPerationsPrint:
    
    def __init__(self, source_data):
        self._source_data = source_data

    def __call__(self, env, epoch):
        count_str = ', '.join([f'{k} : {len(v)}' 
                               for k, v in env.indexes_actions.timeactions.items()])
        print(f'Epoch : {epoch}')
        print(f'''{self._source_data} result\n Profit at end: {env.states_actions.profit},\n{count_str}\n''')
