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
    for fach in os.scandir(video_path):
        if not fach.is_dir(): continue

        e = []
        for vid in os.scandir(fach.path):
            if not vid.is_file(): continue

            e.append({
                'date': datetime.fromtimestamp(os.path.getctime(vid.path)),
                'size': os.path.getsize(vid.path),
                'name': os.path.splitext(vid.name)[0],
                'file': vid.name
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
            'fach': fach
        })
    else:
        abort(404)
