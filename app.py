import os
from datetime import datetime
from flask import Flask, render_template, abort
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

video_path = os.getenv('VIDEO_LOCATION') or '/home/chief/chief-video/videos'

@app.route('/')
def dashboard():
    struc = {}
    faecher = os.listdir(video_path)
    for fach in faecher:
        struc[fach] = []
        for vid in os.listdir(os.path.join(video_path, fach)):
            p = os.path.join(video_path, fach, vid)
            struc[fach].append({
                'date': datetime.fromtimestamp(os.path.getctime(p)),
                'size': os.path.getsize(p),
                'name': vid
            })

    return render_template('Dashboard.html', files=struc)


@app.route('/<string:fach>/<string:name>')
def video(fach, name):
    if os.path.exists(os.path.join(video_path, fach, name)):
        return render_template('Video.html', fach=fach, name=name)
    else:
        abort(404)
