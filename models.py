# imports we will need
import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('plantpal.db')

# UserMixin help import the set of tools for login
class User(UserMixin, Model):
    username = CharField(unique = True)
    email = CharField(unique = True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, email, password):
        try:
            cls.create(
                username=username,
                email=email,
                # this function is from bcrypt
                password=generate_password_hash(password)
                )
        except IntegrityError:
            raise ValueError("user already exists")

class Plant(Model):
    name = CharField(unique = True)
    description = CharField()
    water_interval_in_days = CharField()
    image = CharField(default="https://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/seedling.png")

    class Meta:
        database = DATABASE

    @classmethod
    def create_plant(cls, name, description, water_interval_in_days, image="https://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/seedling.png"):
        try:
            cls.create(
                name=name,
                description=description,
                water_interval_in_days=water_interval_in_days,
                image=image
                )
        except IntegrityError:
            raise ValueError("plant already exists")

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Plant], safe=True)
    DATABASE.close()
