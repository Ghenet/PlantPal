
# import flask framework. g stands for global allows us to use other variable in the project
from flask import Flask, g, request, jsonify
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import check_password_hash
import datetime

import models
import forms

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = "imSoHappyThatArrestedDevelopmentisback.biz"

# setup login_manager with LoginManager class
login_manager = LoginManager()
# setup login_manager to work with our app
login_manager.init_app(app)
# if a user is not logged in, redirect them to login view
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try: 
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database after each connection requesst and send through the response"""
    g.db.close()
    return response

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash('This email does not exist.')
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)    # creates a session and logs in the user
                flash('You have been logged in!', 'success')
                # update the user's plants with new days till_next_water
                return redirect(url_for('profile'))
            else:
                flash('Email or password incorrect.', 'danger')
    return render_template("login.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.RegisterForm()
    # when the form is validated and submitted, create a new user
    if form.validate_on_submit():
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        user = models.User.get(models.User.username == form.username.data)
        login_user(user)
        # redirect user to index
        return redirect(url_for('profile'))
    return render_template("signup.html", form=form)

@app.route('/logout')
# from login_manager login view, will redirect you to the login page
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/profile", methods=["GET", "POST", "PUT"])
@app.route('/profile/<username>')
@login_required
def profile(username=None):
    user = current_user
    # query = models.UsersPlants.select().where(models.UsersPlants.user_id == current_user.id)
    query = models.UsersPlants.select(models.Plant, models.UsersPlants).join(models.Plant).where(models.UsersPlants.user_id == current_user.id)
    for usersplant in query:
        print(usersplant.plant.name)
        print(usersplant.plant.description)
        print(usersplant.date_last_watered)
        print(usersplant.plant.image)
    # plants = user.get_plants()
    # print(user.usersplants)
    dateNow = datetime.datetime.now()
    return render_template("profile.html", user=user, plants=query, dateNow=dateNow)


@app.route('/plants/', methods=['GET', 'POST'])
# @login_required
def plants():
    form = forms.UsersPlantForm()
    plants = models.Plant.select()
    if form.validate_on_submit():
        flash('Plant made', 'success')
        # models.Plant.create_plant(
        #     name=form.name.data,
        #     description=form.description.data,
        #     water_interval_in_days=form.water_interval_in_days.data,
        # )
        return redirect(url_for('profile'))
    return render_template('plants.html', plants=plants, form=form)

@app.route('/users_plants', methods=['GET', 'POST'])
@app.route('/users_plants/<usersplantid>', methods=['GET', 'DELETE'])
def users_plants(usersplantid=None):

    # add in note to retrieve
    if usersplantid == None:
        print('in post')
        for plantid, note in zip(request.form.getlist("plantid[]"), request.form.getlist("notes[]")):
            print("plantid",plantid)
            print("note", note)
            plant = models.Plant.get(models.Plant.id == plantid)
            print("plant",plant)
            print("userid",current_user.id)
            user = models.User.get(models.User.id == current_user.id)
            note=note
            models.UsersPlants.create(
                user=user,
                plant=plant,
                note=note
            )
        return "success"
    else:
        try:
            delete_plant = models.UsersPlants.get(models.UsersPlants.id == usersplantid)
        except:
            raise Exception('Session rollback')
        if delete_plant:
            delete_plant.delete_instance()
            return redirect(url_for('profile'))
        else:
            return "error"
    # return render_template('profile.html', user=current_user)

@app.route('/users_plants/<usersplantid>/water', methods=['GET', 'PUT'])
def water_plant(usersplantid):
    try:
        water_plant = models.UsersPlants.get(models.UsersPlants.id == usersplantid)
    except:
        raise Exception('Session rollback')
    if water_plant:
        water_plant.date_last_watered = datetime.datetime.now()
        water_plant.save()
        # return "watered"
        return redirect(url_for('profile'))
    else:
        return "error"

@app.route('/edit_profile/' , methods=['GET','POST'])
def edit_profile():
    form = forms.EditUserForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.id == current_user.id)
        except:
            raise Exception("Please try again")
        if user:
            print('heyyy work please')
            user.email = form.email.data
            user.username = form.username.data
            user.save()
            return redirect(url_for('profile'))
       
    return render_template('edit_profile.html', form=form)





@app.route('/edit_notes/<usersplantid>', methods =['GET' ,'POST'])
def edit_notes(usersplantid):
    form = forms.UsersPlantForm()
    if form.validate_on_submit():
        try:
            update_plant = models.UsersPlants.get(models.UsersPlants.id == usersplantid)
        except:
            raise Exception("Please try again")
        if user:
            print('heyyy work please')
            update_plant.note = form.note.data
            update_plant.save()
            return redirect(url_for('profile'))
    return render_template('edit_notes.html', form=form)


###########################################################
#################### TESTING ROUTES #######################
###########################################################



@app.route('/user', methods=['GET', 'POST'])
@app.route('/user/<username>', methods=['GET', 'DELETE', 'PUT'])
def user(username=None):

    if username == None and request.method == 'GET':
        return repr(models.User.select().get())
    elif username != None and request.method == 'PUT':
        email = request.json['email']
        # password = form.password.data
        user = models.User.select().where(models.User.username == username).get()
        user.email = email
        user.save()
        return repr(user)
    elif username != None and request.method == 'GET':
        return repr(models.User.select().where(models.User.username==username).get())
    elif username == None and request.method == 'POST':
        created = models.User.create(
            username = request.json['username'],
            email = request.json['email'],
            password = request.json['password']
            )
        user = models.User.select().where(models.User.username == created.username).get()
        return repr(user)
    else: 
        user = models.User.select().where(models.User.username == username).get()
        user.delete_instance()
        return repr(user)

if __name__ == '__main__':
    models.initialize()
    try:
        # models.Plant.create_plant(
        #     name="Beach Spider Lily ",
        #     description="This amazing bulb based plant beach spider lily enjoys environments that are downright aquatic and easy",
        #     water_interval_in_days= 3,
        #     image="https://c8.alamy.com/comp/JAWKW0/beach-spider-lily-JAWKW0.jpg"
        # )
        # models.Plant.create_plant(
        #     name="Bird Of Paradise ",
        #     description="delightfully easy to care for plant that enjoys warm, balmy days year round.",
        #     water_interval_in_days= 5,
        #     image="http://gardeningsolutions.ifas.ufl.edu/images/plants/flowers/bird_paradise.jpg"
        # )
        # models.Plant.create_plant(
        #     name="Eternal Flame",
        #     description="Named Eternal flame for its attractive yellow bract.",
        #     water_interval_in_days= 10,
        #     image="http://www.greenmountainhosta.com/catalog/images/EternalFlame.jpg" 
        # )
        # models.Plant.create_plant(
        #     name="Busy Lizzie",
        #     description="Grown for their attractive blooms outdoors (just about everywhere) and indoors when given enough bright light.",
        #     water_interval_in_days= 14,
        #     image="https://hotemoji.com/images/dl/o/seedling-emoji-by-google.png"
        # )
        # models.Plant.create_plant(
        #     name="Christmas Cactus",
        #     description="The Christmas cactus is the ideal house plant if a grower likes to see flowers blooming from November - January",       
        #     water_interval_in_days= 15,
        #     image="https://pixl.varagesale.com/http://s3.amazonaws.com/hopshop-image-store-production/154471565/9be4b938b57b663aa33328e8e133aa5b.jpg?_ver=large_uploader_thumbnail&w=640&h=640&fit=crop&s=07e705505165f7e6a36a67a04603b420"
        # )
        # models.Plant.create_plant(
        #     name="Elephant's Ear ",
        #     description="A foliage plant with very distinct looking leaves - but it does flower.",
        #     water_interval_in_days= 5,
        #     image="https://www.americanmeadows.com/media/gene-cms/e/l/elephant_ear_container.jpg"
        # )
        # models.Plant.create_plant(
        #     name="Rubber Plant",
        #     description="One of the ficus greats with large glossy oval shaped leaves.",
        #     water_interval_in_days= 6,
        #     image="https://www.houseplantsexpert.com/image-files/ficus_elastica_decora.jpg"
        # )
        # models.Plant.create_plant(
        #     name="Zebra Plant",
        #     description="From the Marantaceae family of plants.",
        #     water_interval_in_days= 9,
        #     image="https://www.houseplantsexpert.com/images/zebrina.jpg"
        # )
        # models.Plant.create_plant(
        #     name="Aluminum Plant",
        #     description="An easy going house plant that is generally simple to please.",
        #     water_interval_in_days= 5,
        #     image="https://www.houseplantsexpert.com/assets/images/pilea-cadierei-1.jpg"
        # )
        # models.Plant.create_plant(
        #     name="ZZ Plant",
        #     description="The worst thing you can do to a ZZ plant is over water it, otherwise it survives well.",
        #     water_interval_in_days= 7,
        #     image="https://www.houseplantsexpert.com/assets/images/zamioculas_zamifolia.jpg"
        # )
        # models.Plant.create_plant(
        #     name="Swiss Cheese Plant ",
        #     description="A great looking foliage plant that grows taller than most indoor plants.",
        #     water_interval_in_days= 8,
        #     image="https://www.houseplantsexpert.com/assets/images/swiss_cheese_plant_leaf.jpg"
        # )
        # models.Plant.create_plant(
        #     name="Watermelon Peperomia",
        #     description="A low growing bushy type plant with striking leaves.",
        #     water_interval_in_days= 5,
        #     image="https://www.houseplantsexpert.com/images/watermelon_peperomia.jpg"
        #     )
        # models.Plant.create_plant(
        #     name="Bird Of Paradise ",
        #     description="delightfully easy to care for plant that enjoys warm, balmy days year round.",
        #     water_interval_in_days= 5,
        #     image="https://hotemoji.com/images/dl/o/seedling-emoji-by-google.png"
        # )
        # models.Plant.create_plant(
        #     name="Tiger Jaws",
        #     description="This species flowers at the end of summer and display jaw like leaves that are toothed.",
        #     water_interval_in_days= 11,
        #     image="https://www.houseplantsexpert.com/assets/images/faucaria_tigrina.jpg"
        # )
        # models.Plant.create_plant(
        #     name="Bunny Ear Cactus  ",
        #     description="The bunny ear cactus, also known as the polka dot cactus is a very popular plant.",
        #     water_interval_in_days= 5,
        #     image="https://www.houseplantsexpert.com/image-files/Opuntia-microdasys.jpg"
        # )
        # models.Plant.create_plant(
        #     name="Sago Palm ",
        #     description="An interesting species which only grows up to 2 feet tall indoors (it's not a palm).",
        #     water_interval_in_days= 5,
        #     image="https://www.houseplantsexpert.com/images/sago_palm.jpg"
        # )
        #  models.Plant.create_plant(
        #     name="Jelly Beans",
        #     description="The Jelly beans displays small finger like succulent leaves that develop red tips.",
        #     water_interval_in_days= 5,
        #     image="https://www.houseplantsexpert.com/assets/images/jelly_beans_plant.jpg"
        # )
        #  models.Plant.create_plant(
        #     name="Croton",
        #     description="Not an easy species to grow, although it's foliage is outstanding in color.",
        #     water_interval_in_days= 6,
        #     image="https://www.houseplantsexpert.com/image-files/croton1.jpg"
        # )
        #  models.Plant.create_plant(
        #     name="Queens Tears",
        #     description="The queens tears is a bromeliad plant which is easy enough for most growers to grow indoors.",
        #     water_interval_in_days= 5,
        #     image="https://www.houseplantsexpert.com/image-files/Billbergia-Nutans.jpg"
        #   )
        #  models.Plant.create_plant(
        #     name="Urn Plant",
        #     description="The Urn plant is also known as the silver vase plant.",
        #     water_interval_in_days= 8,
        #     image="https://www.houseplantsexpert.com/image-files/close-up-urn-plant-flower.jpg"
        #  )
        # models.Plant.create_plant(
        #     name="Boston Fern",
        #     description="One of the easier ferns to grow indoors.",
        #     water_interval_in_days= 8,
        #     image="https://www.houseplantsexpert.com/assets/images/boston_ferns_in_hanging_baskets_1.jpg"
        #  )
        models.Plant.create_plant(
            name="Aloe Vera",
            description="The Aloe Vera is a common house plant that has many potential heath benefits. An indoor Aloe is easy to grow and not demanding.",
            water_interval_in_days= 8,
            image="https://www.houseplantsexpert.com/assets/images/aloe-foliage-1.jpg"
         )
        # print('created plant')
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT)
