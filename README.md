# Docker Flask Project

A proof of concept project, taking an old project and using Docker to run it locally

## How To Download
```
docker run --name repo alpine/git clone https://github.com/tristann3/docker-flask-project
```
```
docker build -t flask-image .
```
```
docker run -p 5000:5000 --rm --name flask-container flask-image
```
