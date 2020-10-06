from collections import defaultdict

class TimeActions:
    def __init__(self):
        self._timeactions = None
        self.reset()

    @property
    def timeactions(self):
        return dict(sorted(self._timeactions.items()))

    def save(self, action, time, done, n_stocks=None, frac=None):

        if (n_stocks is None and frac is None) or (n_stocks and frac):
            raise ValueError('You must pass n_stocks or frac parameters')
        
        if action == 'no_action':
            key = action 
        else:
            key = self._build_key_n_stocks(action, done, n_stocks) if n_stocks\
                else self._build_key_n_frac(action, done, frac)  

        self._timeactions[key].append(time)

    def reset(self):
        self._timeactions = defaultdict(list)

    def _build_key_n_stocks(self, action, done, n_stocks):
        return f'{self._map_done(done)}{action}_{n_stocks}_stocks'

    def _build_key_n_frac(self, action, done, frac):
        return f'{self._map_done(done)}{action}_{frac*100}%' if frac != 1 \
            else f'{self._map_done(done)}{action}_all'

    @staticmethod
    def _map_done(done):
        return '' if done else 'pred_'
