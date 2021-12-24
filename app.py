import os
from datetime import datetime
from flask import Flask, render_template, abort, redirect, flash, url_for
from dotenv import load_dotenv
from flask_login.utils import login_required, logout_user
from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_login import LoginManager, UserMixin, login_user, current_user


######################
######## SETUP #######
######################


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Bitte anmelden"

VIDEO_PATH = os.getenv('VIDEO_LOCATION') or './videos'
VIDEO_URL = os.getenv('VIDEO_URL') or '/videos'
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

######################
######## UTIL ########
######################


class User(UserMixin):
    id = 1
    authenticated = False

    @property
    def is_authenticated(self):
        return self.authenticated


# user = User()


@login_manager.user_loader
def load_user(id):
    return User()


class LoginForm(FlaskForm):
    password = PasswordField(label="Passwort eingeben",
                             validators=[DataRequired()])
    submit = SubmitField(label="Einloggen")

######################
####### ROUTES #######
######################


@app.route('/')
@login_required
def dashboard():
    struc = {}
    for fach in os.scandir(VIDEO_PATH):
        if not fach.is_dir():
            continue

        e = []
        for vid in os.scandir(fach.path):
            if not vid.is_file():
                continue

            e.append({
                'date': datetime.fromtimestamp(os.path.getctime(vid.path)),
                'size': os.path.getsize(vid.path),
                'name': os.path.splitext(vid.name)[0],
                'file': vid.name,
            })

        struc[fach.name] = sorted(e, key=lambda ele: ele['name'])

    return render_template('Dashboard.html', files=struc)


@app.route('/<string:fach>/<string:vid>')
@login_required
def video(fach, vid):
    p = os.path.join(VIDEO_PATH, fach, vid)
    if os.path.exists(p) and os.path.isfile(p):
        return render_template('Video.html', vid={
            'date': datetime.fromtimestamp(os.path.getctime(p)),
            'size': os.path.getsize(p),
            'name': os.path.splitext(vid)[0],
            'file': vid,
            'fach': fach,
            #            'url': f"{video_url}/{fach}/{vid}" if password and username else f"{video_url}/{fach}/{vid}"
        })
    else:
        abort(404)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = try_login(form.password.data)
        if login_user(user, remember=True):
            flash("Erfolgreich angemeldet")
            return redirect(url_for('dashboard'))
        else:
            flash("Falsches Passwort")
    return render_template("Login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("dashboard"))



def try_login(password):
    user = User()
    if password == PASSWORD:
        user.is_authenticated = True
    return user
