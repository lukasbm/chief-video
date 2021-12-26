# Streaming Server

This directory provides a preconfigured streaming server.
It used nginx with a plugin to convert rtmp streams to http streams.

## Build
```bash
docker build -t boehmls/streaming-server:latest .
```

## Run
- Development: `docker run --rm -it -p 3456:1935 -p 3457:8080 -p 3458:80 boehmls/streaming-server:latest`
- Deployment: `docker run --rm -d -p 1935:1935 -p 8080:8080 --name streaming-server boehmls/streaming-server:latest`

## TODO
- Streamline and optimize images using Docker multistage builds
