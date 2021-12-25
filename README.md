# ChiefVideo

Simple website for videos playing hosted videos

## Developing

### Native

#### Simple development HTTP server

we can provide a simple http server by changing into the video directory and call `python3 -m http.server`

#### Simple flask server

by running `python3 -m flask run` we can start a simple development server for the web app

### Docker

```bash
docker build -t boehmls/chief-video:latest .
docker run --rm --it -v <VIDEO_LOCATION>:/app/videos -p <PORT>:5000 -e "VIDEO_URL=<VIDEO_URL>" boehmls/chief-video:latest
```

## Deploying

The docker deployment is recommended.

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
docker run --name chief-video -v <VIDEO_PATH>:/app/videos -p <PORT>:5000 --env-file <ENV_FILE>  boehmls/chief-video:latest
```

where `<VIDEO_PATH>` is the absolute path to the video directory.
The `<PORT>` can be any of your choice. Note that the port is only for the docker process running on the localhost. You still have to forward it using a reverse proxy like nginx.
Then we need to pass the environment variables. We can do this by hand or use an `.env` file like `<ENV_FILE>`.

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
- `VIDEO_URL`: the base url to videos. Since the flask app does not provide the videos themselves, we need another HTTP server to do this job. This variable needs to provide the resources in the same tree structure as presented in the directory section. Either has to be a relative path or a full url (including the "http://")
- `SECRET_KEY`: required by flask to use secure sessions
- `LOGIN_PASSWORD`: password for the website
- `VIDEO_USERNAME` and `VIDEO_PASSWORD`: are the http basic auth information for the video streaming server. Can be omitted if not neccecary

## Roadmap

- [x] better authentication (not just basic http)
- [x] search functionality
- [ ] option to setup without a website password
- [ ] Live streaming
- [ ] video upload (in website)
- [ ] configuration files (to possibly exclude some files or set other information)
- [ ] allowing to use a remote vide directory
- [ ] show videolength (using ffmpeg - ffprobe)
- [ ] converter for new video files (as not all video formats are supported in every browser)
- [ ] update design
