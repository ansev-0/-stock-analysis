from src.app.config import Config
from itsdangerous.url_safe import URLSafeTimedSerializer


class EmailRegisterToken:
    _url_safe_token_maker = URLSafeTimedSerializer(Config.SECRET_KEY)
    _salt = 'email-confirm'
    _max_age = 3600

    def create(self, email):
        return self._url_safe_token_maker.dumps(email, salt=self._salt)

    def loads(self, token):
        return self._url_safe_token_maker.loads(token, max_age=self._max_age, salt=self._salt)