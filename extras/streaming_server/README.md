# Streaming Server

This directory provides a preconfigured streaming server.
We are using nginx http server with a plugin to convert rtmp streams to http streams.

## Build
```bash
docker build -t boehmls/streaming-server:latest .
```

## Run
- Development: `docker run --name streaming-server-dev --rm -it -p 3456:1935 -p 3457:8080 -p 3458:80 boehmls/streaming-server:latest`
- Deployment: `docker run --rm -d -p 1935:1935 -p 8080:8080 --name streaming-server boehmls/streaming-server:latest`

## Inspect
- Logs: `docker logs streaming-server-dev`
- SSH into container: `docker exec -it streaming-server-dev /bin/bash`

## TODO
- Streamline and optimize images using Docker multistage builds
