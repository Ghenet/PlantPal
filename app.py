
# import flask framework. g stands for global allows us to use other variable in the project
from flask import Flask, g, request, jsonify
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_bcrypt import check_password_hash

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
                flash('Login was successful', 'success')
                # update the user's plants with new days till_next_water
                return redirect(url_for('profile'))
            else:
                flash('Email or password incorrect.')
    return render_template("login.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.RegisterForm()
    # when the form is validated and submitted, create a new user
    if form.validate_on_submit():
        flash('Yay you registered', 'success')
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
    flash("You are logged out", "success")
    return redirect(url_for('index'))


@app.route("/profile", methods=["GET", "POST", "PUT"])
@app.route('/profile/<username>')
@login_required
def profile(username=None):
    user = current_user
    # user.
    return render_template("profile.html", user=user)


@app.route('/plants/', methods=['GET', 'POST'])
# @login_required
def plants():
    form = forms.PlantForm()
    plants = models.Plant.select()
    if form.validate_on_submit():
        flash('Plant made', 'success')
        models.Plant.create_plant(
            name=form.name.data,
            description=form.description.data,
            water_interval_in_days=form.water_interval_in_days.data,
        )
        return redirect(url_for('profile'))
    return render_template('plants.html', plants=plants, form=form)

@app.route('/users_plants', methods=['GET', 'POST'])
def users_plants():
    # user = current_user
    # print(request.form)
    # print(request.form.getlist("plantid[]"))
    for plantid in request.form.getlist("plantid[]"):
        print("plantid",plantid)
        plant = models.Plant.get(models.Plant.id == plantid)
        print("plant",plant)
        print("userid",current_user.id)
        user = models.User.get(models.User.id == current_user.id)
        models.UsersPlants.create(
            user=user,
            plant=plant
        )
    return render_template('profile.html', user=current_user)



# @app.route('/plants/', methods=['GET', 'DELETE'])
# # @login_required
# def deleteplants():
#     form = forms.PlantForm()
#     db = get_db()
#     db.execute('delete from entries where id=' + entry_id)
#     db.commit()
#     flash('Entry deleted')
#         )
#         return redirect(url_for('profile'))
#     return render_template('plants.html', form=form)
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
        models.Plant.create_plant(
            name="Spikey plant",
            description="This is a spikey plant.",
            water_interval_in_days= 20,
            image="https://hotemoji.com/images/dl/o/seedling-emoji-by-google.png"
        )
        print('created plant')
    except ValueError:
        pass
    app.run(debug=DEBUG, port=PORT)
