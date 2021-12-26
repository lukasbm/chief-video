# Streaming Server

This directory provides a preconfigured streaming server.
It used nginx with a plugin to convert rtmp streams to http streams.

## Build
```bash
docker build -t boehmls/streaming-server:latest .
```

## Run
```bash
docker run --rm -it boehmls/streaming-server:latest
```

## TODO
- Streamline and optimize images using Docker multistage builds
