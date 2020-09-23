import numpy as np

class ColorsIntensistyRGB:

    colors_arr = np.array([[1,0,0], [0,0,1], [0,1,0]], dtype=np.int8)
    
    def __init__(self, min_intensity):
        self.min_intensity = min_intensity
    
    def get_colors(self, n_red, n_blues, n_green):
        
        interval_colors = np.concatenate(tuple(map(self._get_intervals_colors,
                                                 (n_red, n_blues, n_green))))[:, None]
        base_colors = self._get_base_colors(n_red, n_blues, n_green)
        return self._build_colors(base_colors, interval_colors)
        
    def _get_intervals_colors(self, n):
        return np.linspace(start=1, stop=self.min_intensity, num=n)[::-1]
    
    def _build_colors(self, base_colors, interval_colors):
        return tuple(map(tuple, np.concatenate((base_colors, interval_colors), axis=1)))
    
    def _get_base_colors(self, *args):
        return np.repeat(self.colors_arr, args, axis=0)