# imports we will need
import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('plantpal.db')

# UserMixin help import the set of tools for login


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
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
    name = CharField(unique=True)
    description = CharField()
    water_interval_in_days = CharField()
    image = CharField(
        default="https://s3.amazonaws.com/pix.iemoji.com/images/emoji/apple/ios-12/256/seedling.png")

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


class UserPlant(Model):
    user = ForeignKeyField(User, backref="userplants")
    plant = ForeignKeyField(Plant, backref="userplants")
    last_watered = DateTimeField(default=datetime.datetime.now())
    notes = CharField()

    class Meta:
        database = DATABASE


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Plant, UserPlant], safe=True)
    # user = User.get(User.username == "user1")
    # plant = Plant.get(Plant.name == "cats")
    # user = User.get(User.username == "user3")
    # plant = Plant.get(Plant.name == "bears")
    # UserPlant.create(user=user, plant=plant, notes="Bedroom plant")
    # UserPlant.select().delete()
    # user_seeds = (
    #     {'username': 'user1', "email": "abc@abc.com", "password": "123"},
    #     {'username': 'user2', "email": "abcd@abc.com", "password": "123"},
    #     {'username': 'user3', "email": "abcde@abc.com", "password": "123"},
    # )
    # for user in user_seeds:
    #     User.create_user(
    #         username=user["username"],
    #         email=user["email"],
    #         password=user["password"],
    #     )
    DATABASE.close()
