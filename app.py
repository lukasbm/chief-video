import os
from datetime import datetime
from flask import Flask, render_template, abort, redirect, flash
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

video_path = os.getenv('VIDEO_LOCATION') or './videos'
video_url = os.getenv('VIDEO_URL') or '/videos'
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')


class LoginForm(FlaskForm):
    password = PasswordField(label="Passwort eingeben", validators=[DataRequired()])
    submit = SubmitField(label="Einloggen")


@app.route('/')
def dashboard():
    struc = {}
    for fach in os.scandir(video_path):
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
def video(fach, vid):
    p = os.path.join(video_path, fach, vid)
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
        return redirect('dashboard')
    else:
        flash("Falsches Passwort")
        return render_template("Login.html", form=form)


@app.route('/logout')
def logout():
    pass
