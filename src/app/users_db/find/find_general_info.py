from src.app.users_db.find.find import FindDataBaseUsers
from src.app.users_db.database import DataBaseUsersGeneralInfo

class FindGeneralInfoDataBaseUsers(DataBaseUsersGeneralInfo, FindDataBaseUsers):

    def find_by_username(self, username, **kwargs):
        return self.find_one_by_field('username', username)

    def find_by_email(self, email, **kwargs):
        return self.find_one_by_field('email', email, **kwargs)

    def find_by_phone_number(self, phone_number, **kwargs):
        return self.find_one_by_field('phone_number', phone_number, **kwargs)

    def find_one_by_field(self, field, value_field, **kwargs):
        return self.find_one({field : value_field}, **kwargs)

    def find_many_by_field(self, field, value_field, **kwargs):
        return self.find({field : value_field}, **kwargs)

    def exist_username_in_db(self, username):
        return self.exist('username', username)

    def exist_email_in_db(self, email):
        return self.exist('email', email)

    def exist_phone_number_in_db(self, phone_number):
        return self.exist('phone_number', phone_number)

    def exist(self, field, value_field):
        return self.find_one_by_field(field, value_field) is not None

    def exist_with_password(self, password, field, value_field):
        return self.find_one({'password' : password, field : value_field}) is not None

    def exist_username_with_password(self, username, password):
        return self.exist_with_password(password, 'username', username)

    def exist_email_with_password(self, email, password):
        return self.exist_with_password(password, 'email', email)

    def exist_phone_number_with_password(self, phone_number, password):
        return self.exist_with_password(password, 'phone_number', phone_number)
