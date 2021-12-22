# ChiefVideo

Simple website for videos playing hosted videos

## Developing

### Native

#### Simple development HTTP server
we can provide a simple http server by changing into the video directory and call `python3 -m http.server`

#### Simple flask server
by running `python3 -m flask run` we can start a simple development server for the web app

### Docker
TODO
```bash
docker build -t chief-video:latest .
```

## Deploying

### Native
The following assumes a linux server with systemd, nginx and python3 installed.
First you have to adapt the `chief-video.server` and `chief-video.conf` to your liking and update paths as neccecary.
```bash
pip3 install gunicorn
sudo ln -s ./chief-video.service /etc/systemd/system/chief-video.service
sudo daemon-reload
sudo ln -s ./chief-video.conf /etc/nginx/sites-enabled/chief-video.conf
sudo systemctl start chief-video
sudo systemctl reload nginx
```

### Docker

```bash
docker pull boehmls/chief-video:latest
docker run --name chief-video -v <VIDEO_FOLDER>:/app/videos -p <PORT>:5000 boehmls/chief-video:latest
```

where `<VIDEO_FOLDER>` is the directory on the host system. This variable is usually also the same as the `VIDEO_LOCATION` env variable

## Directory

The video directory has to be structured as follows:

```
. // video root
|- Category1
|  |- Video1
|  |- Video2
|- Category2
|  |- Video1
|  |- Video2
|- ...
```

## Environment Variables
- `VIDEO_LOCATION`: the (absolute) path on the server where the videos are located. Default `./videos`
- `VIDEO_URL`: the base url to videos. Since the flask app does not provide the videos themselves, we need another HTTP server to do this job. This variable needs to provide the resources in the same tree structure as presented in the directory section.
