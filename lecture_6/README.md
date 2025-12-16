# Dockerized Book Collection API

Full-featured Book Collection API (from lecture_5) containerized with Docker, including required healthcheck endpoint.

## Requirements

1. Docker installed
2. Docker Compose (optional)

## Step-by-Step Guide (Docker Requirements)

### 1. Build docker image
```bash
docker build . -t app:latest
```
### 2. Check the newly created image
You should see the app image with tag latest in the list.
```bash
docker images
```
### 3. Start container from the newly built docker image
```bash
docker run app:latest
```
_Note: For port mapping, use: docker run -p 8000:8000 app:latest_
### 4. Check that your container is running in another terminal tab
Open a new terminal tab and run:
```bash
docker ps
```
You should see the running container with image app:latest.
### 5. Query the endpoint of the application
Make sure you receive {"status": "ok"} response:
```bash
curl http://localhost:8000/healthcheck
```
Or open in browser: http://localhost:8000/healthcheck
### 6. Go inside the container
Explore the filesystem with ls and cd commands:
```bash
docker exec -it <container-id> bash
```
### 7. Stop the container and check the container status
```bash
docker stop <container-id>
docker ps -a
```
## Alternative: Using Docker Compose
### 1. Build and start with Docker Compose
```bash
docker-compose up --build
```
### 2. Stop containers
```bash
docker-compose down
```