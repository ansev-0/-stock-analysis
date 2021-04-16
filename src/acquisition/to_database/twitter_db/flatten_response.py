class FlattenResponse:
    
    def __init__(self, decode_map):
        self.decode_map = decode_map
        self._response = None
        self._items = {}
        
    def one(self, response):
        self._response = response
        self._decode_branch()
        output = self._items
        self._items = {}
        return output

    def many(self, list_response):
        return list(map(self.one, list_response))
     
    def _decode_branch(self, decode_map=None, prefix=None, response=None):
        # set params
        prefix = self._assign_if_not_null_else(prefix, '')
        decode_map = self._assign_if_not_null_else(decode_map, self.decode_map)
        response = self._assign_if_not_null_else(response, self._response)
        # get items
        for item in decode_map:
            if isinstance(item, str):
                try:
                    self._items[f'{prefix}{item}'] = getattr(response, item)
                except Exception as error:
                    self._items[f'{prefix}{item}'] = error             
            elif isinstance(item, dict):
                self._decode_branches(item, response)
                
    def _decode_branches(self, branches, response):
        for prefix, decode_map in branches.items():
            self._decode_branch(decode_map, f'{prefix}_', getattr(response, prefix))
            
    @staticmethod        
    def _assign_if_not_null_else(value, value_default):
        return value if value is not None else value_default
            