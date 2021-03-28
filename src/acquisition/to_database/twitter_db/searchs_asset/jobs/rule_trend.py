class RuleTrend:

    def ___init__(self, retweet_count_f, favorite_count_f, user_followers_f, repeat_f):

        self.retweet_count_f = retweet_count_f
        self.favorite_count_f = favorite_count_f
        self.user_followers_f = user_followers_f
        self.repeat_f = repeat_f

    def __call__(self, word, list_response):
        factor = sum(list(map(self._calculate_ind, list_response)))
        indices = [None, *self._get_indices(list_response), None, None]

        return [
            {'word' : word,
             'id2' : id2,
             'id1' : id1,
             'factor_priority' : factor * (self.repeat_f ** n),
                 }
            for n, (id2, id1) in enumerate(zip(indices[:-1], indices[1:]))]
            
    def _calculate_ind(self, response):
        return self.retweet_count_f * response.retweet_count + \
        self.favorite_count_f * response.favorite_count + \
        self.user_followers_f * response.user.followers_count 

    def _get_indices(self, list_response):
        return sorted(list(map(lambda response : response.id, list_response)), reverse=True)