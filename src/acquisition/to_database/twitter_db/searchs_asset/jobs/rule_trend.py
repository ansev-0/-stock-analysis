class RuleTrend:

    def __init__(self, retweet_count_f=5e-4, 
                        favorite_count_f=1e-4, 
                        user_followers_f=1e-5, 
                        repeat_f=0.95,
                        min_factor=120,
                        repeat_fail_factor=10000,
                        current_search_priority=2,
                        ):

        self.retweet_count_f = retweet_count_f
        self.favorite_count_f = favorite_count_f
        self.user_followers_f = user_followers_f
        self.repeat_f = repeat_f
        self.min_factor = min_factor
        self.repeat_fail_factor = repeat_fail_factor
        self.current_search_priority = current_search_priority
        self._since_id = None
        self._max_id  = None

    def __call__(self, word, since_id, max_id, list_response):

        self._since_id = since_id
        self._max_id = max_id

        if isinstance(list_response, str) or len(list_response) == 0 or \
            any(map(lambda resp: isinstance(resp, str), list_response)):

            return [self._build_dict_job(word, self.repeat_fail_factor * self.current_search_priority)]
        else:
            #calculate factor
            factor = sum(list(map(self._calculate_ind, list_response)))

            return [self._build_dict_job(word, factor * self.current_search_priority)] +  \
            (self._not_empty_response(word, list_response, factor) if factor > self.min_factor
                 else [])

    def _build_dict_job(self, word, factor, since_id=None, max_id=None):
        return {'word' : word,
                'max_id' : max_id if max_id is not None else self._max_id,
                'since_id' : since_id if since_id is not None else self._since_id,
                'factor_priority' : factor,
                 }

    def _not_empty_response(self, word, list_response, factor):
        indices = [self._max_id, *self._get_indices(list_response), self._since_id]

        return [self._build_dict_job(word, factor * (self.repeat_f ** n), since_id, max_id)
                for n, (max_id, since_id) in enumerate(zip(indices[:-1], indices[1:]))]
            
    def _calculate_ind(self, response):
        return self.retweet_count_f * response.retweet_count + \
        self.favorite_count_f * response.favorite_count + \
        self.user_followers_f * response.user.followers_count 

    def _get_indices(self, list_response):
        return sorted(list(map(lambda response : response.id, list_response)), reverse=True)