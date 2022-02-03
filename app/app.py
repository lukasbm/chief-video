import functools
import os
from datetime import datetime
from flask import Flask, render_template, abort, redirect, flash, url_for, session
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_session import Session
from datetime import timedelta
from ffprobe import FFProbe
import werkzeug.exceptions

######################
######## SETUP #######
######################


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

Session(app)

VIDEO_PATH = os.getenv('VIDEO_PATH') or '../videos'
VIDEO_URL = os.getenv('VIDEO_URL') or '/videos'
VIDEO_USERNAME = os.getenv('VIDEO_USERNAME')
VIDEO_PASSWORD = os.getenv('VIDEO_PASSWORD')
LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD')


@app.context_processor
def set_context():
    def current_authentication():
        try:
            return session["authenticated"]
        except KeyError:
            return False
    return {"authenticated": current_authentication()}

######################
######## UTIL ########
######################


class LoginForm(FlaskForm):
    password = PasswordField(label="Passwort eingeben",
                             validators=[DataRequired()])
    submit = SubmitField(label="Einloggen")


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if session["authenticated"] == True:
                return func(*args, **kwargs)
            else:
                return redirect(url_for("login"))
        except KeyError:
            return redirect(url_for("login"))
    return wrapper

######################
####### ROUTES #######
######################


@app.route('/')
def index():
    return render_template("Index.html")


@app.route("/videos")
@login_required
def videos():
    files = []
    for category in os.scandir(VIDEO_PATH):
        if not category.is_dir():
            continue

        for vid in os.scandir(category.path):
            if not vid.is_file():
                continue


            duration = "not available"
            # try:
            #     metadata = FFProbe(vid.path)
            #     if len(metadata.streams) < 1 or sum([1 if s.is_video() else 0 for s in metadata.streams]) != len(metadata.streams):
            #         continue
            #     if "Duration" not in metadata.metadata:
            #         continue
            #     duration = metadata.metadata["Duration"]
            # except:
            #     continue

            files.append({
                'date': datetime.fromtimestamp(os.path.getctime(vid.path)).strftime('%d.%m.%Y - %H:%M'),
                'size': os.path.getsize(vid.path),
                'name': os.path.splitext(vid.name)[0],
                'file': vid.name,
                'category': category.name,
                'duration': duration
            })

    return render_template('Videos.html', files=files)


@app.route('/videos/<string:category>/<string:vid>')
@login_required
def video(category, vid):
    p = os.path.join(VIDEO_PATH, category, vid)

    if VIDEO_USERNAME and VIDEO_PASSWORD:
        url = VIDEO_URL.split("://")
        if len(url) != 2:
            abort(500)
        url = f"{url[0]}://{VIDEO_USERNAME}:{VIDEO_PASSWORD}@{url[1]}/{category}/{vid}"
    else:
        url = f"{VIDEO_URL}/{category}/{vid}"

    if os.path.exists(p) and os.path.isfile(p):
        return render_template('Video.html', vid={
            'date': datetime.fromtimestamp(os.path.getctime(p)),
            'size': os.path.getsize(p),
            'name': os.path.splitext(vid)[0],
            'file': vid,
            'category': category,
            'url': url
        })
    else:
        abort(404)


@app.route("/streams")
@login_required
def streams():
    return render_template("Streams.html")


########################
#### UTILITY ROUTES ####
########################

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == LOGIN_PASSWORD:
            session["authenticated"] = True
            flash("Erfolgreich angemeldet")
            return redirect("/")
        else:
            flash("Falsches Passwort")
    return render_template("Login.html", form=form)


@app.route("/logout", methods=["POST"])
def logout():
    try:
        session["authenticated"] = False
    except KeyError:
        pass
    return redirect("/")


@app.errorhandler(werkzeug.exceptions.HTTPException)
def handle_http_error(e):
    return render_template("Error.html", e=e)
