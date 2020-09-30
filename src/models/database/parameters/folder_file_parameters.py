import re
import numpy as np
import os

class FolderProperties:
    
    def __init__(self, path, base_name, ext):
        
        self._path = path
        self._ext = ext
        self._base_name = base_name
        self._check_only_elements_ext()

        
    @property
    def path(self):
        return self._path
        
    @property
    def ext(self):
        return self._ext
        
    @property
    def base_name(self):
        return self._base_name
    
    @property
    def elements(self):
        return os.listdir(self.path)
        
    @property
    def n_elements(self):
        return len(self.elements)
    
        
    @property
    def number_next_element(self):
        n_elements = self.n_elements
        return self._calculate_next_element(n_elements) if n_elements > 0  else 0

    @property   
    def name_next_element(self):
        return f'{self._base_name}_{self.number_next_element}{self._ext}'
    
    @property
    def total_size(self):
        
        return sum(
                   map(
                       lambda file: os.path.getsize(os.path.join(self.path, file)), 
                       os.listdir(self.path)
                      )
                  )
    
    def remove(self, file):
        os.remove(os.path.join(self.path, file))
    
    def _calculate_next_element(self, n_files):
        diff = np.setdiff1d(
                            range(n_files), 
                            tuple(map(self._extract_number, os.listdir(self._path)))
        )
        return n_files if len(diff) == 0 else diff[0]
    
    
    def _extract_number(self, file_name):
        return int(re.findall(rf'(\d+){self.ext}', file_name)[0])
    
    def _check_only_elements_ext(self):
        
        if not np.all(
            tuple(
                  map(
                          lambda file: file.endswith(self._ext), 
                           os.listdir(self._path)
                     )
                 )
                     ):
            
            raise TypeError(f'Path {self._path} has not only {self._ext} files')
    

