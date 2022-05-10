import datetime
import sqlalchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    events = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    friends_list = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    friends_requests = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}> id={self.id} name={self.name} email={self.email}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def delete_from_friends_requests(self, friend_name):
        if self.friends_requests.find(friend_name) == 0:
            self.friends_requests = list(self.friends_requests)

            for i in range(0, len(friend_name) + 1):
                self.friends_requests[i] = ''

            self.friends_requests = ''.join(self.friends_requests)

        elif self.friends_requests.find(friend_name) == -1:
            pass

        else:
            index = self.friends_requests.find(friend_name)
            self.friends_requests = list(self.friends_requests)

            for i in range(index - 1, index + len(friend_name)):
                self.friends_requests[i] = ''

            self.friends_requests = ''.join(self.friends_requests)

    def accept_friend(self, friend_name):
        self.delete_from_friends_requests(friend_name)

        if self.friends_list:
            self.friends_list += f';{friend_name}'
        else:
            self.friends_list = friend_name

    def deny_friend(self, friend_name):
        self.delete_from_friends_requests(friend_name)

    def add_friend_request(self, friend_name):
        if self.friends_requests:
            if friend_name not in self.friends_requests:
                self.friends_requests += f';{friend_name}'
        else:
            self.friends_requests = f'{friend_name}'
