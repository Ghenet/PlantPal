# imports we will need
import datetime
from peewee import *

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

DATABASE = SqliteDatabase('plant-pal.db')

# UserMixin help import the set of tools for login


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = DATABASE

    @classmethod
    def update_user(cls, userid, email):
        user = User.select().where(user.id == userid).get()
        user['email'] = email
        user.save()
        return jsonify(user)

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

    def __repr__(self):
        return "{}, {}, {}, {}".format(
            self.id,
            self.username,
            self.email,
            self.joined_at,
        )

    # get all the plants that belong to a user from the join table
    # def get_plants(self):
    #     return UsersPlants.select().where(UsersPlants.user == self).get()

    # def get_stream(self):
    #     return UsersPlants.select().where(UsersPlants.user == self).get()

    # DELETE
    # to delete a user, delete all their plants first, then delete them from db

    # PUT
    # find the same user that matches self and update based on form data

    # DELETE
    # def delete_users_plant(self, plant):
    # this method should be called like current_user.delete_users_plant(plant.name)
    # the plant name should come from form data on the front end
        # get the user's plant based on self==user and plant==plant.name
        # delete_instance() of the user's plant
        # get all the plants that belong to the user now
        # return those plants to app to be rendered

    # PUT
    # def update_users_plant_note(self, plant, note):
    # this method should be called like current_user.update_users_plant(plant.name, note)
    # the plant name should come from form data on the front end
        # get the user's plant based on self==user and plant==plant.name
        # update the user's plant note
        # save
        # return the plant

    # PUT
    # def water_users_plant(self, plant, date_watered):
    # date_watered should be the time when the request is made
        # get the user's plant from the self==user, plant==plant.name
        # update the plant's date_last_watered
        # probably need to do some weird date time math here
        # save
        # return the plant


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


class UsersPlants(Model):
    note = CharField(max_length=150)
    date_added = DateTimeField(default=datetime.datetime.now())
    date_last_watered = DateTimeField(default=datetime.datetime.now())
    days_till_next_water = IntegerField(default=0)
    user = ForeignKeyField(model=User, backref='usersplants')
    plant = ForeignKeyField(model=Plant, backref='usersplants')

    class Meta:
        database = DATABASE

    # POST
    @classmethod
    def create_users_plant(cls, note, user, plantid):
        # the note should come from the front end form
        plant = Plant.select().where(Plant.id == plantid)
        try:
            cls.create(
                note=note,
                user=user,
                plant=plant
            )
        except IntegrityError:
            raise ValueError("error")
    # @classmethod
    # def create_users_plant(cls, note, user, plant):
        # the note should come from the front end form
        # the user should just be current_user
        # the plant could come from the front end form
        # error handling goes here


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Plant, UsersPlants], safe=True)
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
