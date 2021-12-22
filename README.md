# ChiefVideo

Simple website for videos playing hosted videos

## Developing

### Native

TODO

### Docker

```bash
docker build -t my-python-app .
docker run -it --rm --name my-running-app my-python-app
```

## Deploying

### Native

TODO

### Docker

```bash
docker pull boehmls/chief-video:latest
docker run --name chief-video boehmls/chief-video:latest -v <VIDEO_FOLDER>:/app/videos
```

where `<VIDEO_FOLDER>` is the directory on the host system.

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
