class RuleTrend:

    def __init__(self, retweet_count_f=5e-4, 
                        favorite_count_f=1e-4, 
                        user_followers_f=1e-5, 
                        repeat_f=0.95):

        self.retweet_count_f = retweet_count_f
        self.favorite_count_f = favorite_count_f
        self.user_followers_f = user_followers_f
        self.repeat_f = repeat_f

    def __call__(self, word, list_response):
        #calculate factor
        factor = sum(list(map(self._calculate_ind, list_response)))

        return self._not_empty_response(word, list_response, factor) \
            if isinstance(list_response, list) and len(list_response) > 0 \
                else [self._build_dict_job(word, since_id, max_id, factor)]

    def _build_dict_job(self, word, since_id, max_id, factor):
        return {'word' : word,
                'max_id' : max_id,
                'since_id' : since_id,
                'factor_priority' : factor,
                 }

    def _not_empty_response(self, word, list_response, factor):
        indices = [None, *self._get_indices(list_response), None, None]

        return [self._build_dict_job(word, since_id, max_id, factor * (self.repeat_f ** n))
                for n, (max_id, since_id) in enumerate(zip(indices[:-1], indices[1:]))]
            
    def _calculate_ind(self, response):
        return self.retweet_count_f * response.retweet_count + \
        self.favorite_count_f * response.favorite_count + \
        self.user_followers_f * response.user.followers_count 

    def _get_indices(self, list_response):
        return sorted(list(map(lambda response : response.id, list_response)), reverse=True)
        