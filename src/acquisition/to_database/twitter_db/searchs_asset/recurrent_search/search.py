from src.acquisition.to_database.twitter_db.searchs_asset.to_database import TwitterSearchToDataBases

class RecurrentSearch:
    _to_db = TwitterSearchToDataBases()

    def __init__(self, min_fav, min_retweet, min_followers):
        self.min_fav = min_fav
        self.min_retweet = min_retweet
        self.min_followers = min_followers

    def __call__(self, word):
        self._make_request(word)

    def _make_request(self, word, since_id=None, max_id=None):
        #make request
        response = self._to_db(word, since_id=since_id, max_id=max_id)
        if response is None or not response:
            return []

        to_output = list(
                map(lambda obj_response: 
                    (obj_response.retweet_count,
                     obj_response.favorite_count,
                     obj_response.user.followers_count),
                    response
                    )
            )
        if not self._need_new_request(response):
            return to_output

        ids = self._get_ids(response)
        if not ids:
            return []

        ids = [None, *ids, None]

        for id2, id1 in zip(ids[:-1], ids[1:]):
            next_request = self._make_request(word, id1, id2)
            to_output += next_request 
        return to_output

    @staticmethod
    def _get_ids(response):
        return sorted(map(lambda obj: obj.id, response), reverse=True)
    
    def _need_new_request(self, response):
        return any(
            map(lambda obj_response: 
                   obj_response.retweet_count > self.min_retweet or
                   obj_response.favorite_count > self.min_fav or
                   obj_response.user.followers_count > self.min_followers, 
                response)
        )

#recurrent = RecurrentSearch(50, 50, 25000)
#recurrent('google')
