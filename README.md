# ChiefVideo

Simple website for videos playing hosted videos

## Developing

### Native

TODO

### Docker

```bash
docker build -t chief-video:latest .
```

## Deploying

### Native

TODO

### Docker

```bash
docker pull boehmls/chief-video:latest
docker run --name chief-video -v <VIDEO_FOLDER>:/app/videos -p <PORT>:5000 boehmls/chief-video:latest
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
