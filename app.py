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
                'name': os.path.splitext(vid)[0],
		        'file': vid
            })

    return render_template('Dashboard.html', files=struc)


@app.route('/<string:fach>/<string:vid>')
def video(fach, vid):
    p = os.path.join(video_path, fach, vid)
    if os.path.exists(p):
        return render_template('Video.html', vid={
            'date': datetime.fromtimestamp(os.path.getctime(p)),
            'size': os.path.getsize(p),
            'name': os.path.splitext(vid)[0],
            'file': vid,
            'fach': fach
        })
    else:
        abort(404)
