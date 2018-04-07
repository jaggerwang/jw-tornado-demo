# JW Tornado Demo

A python api server demo developed using tornado web framework, deploy with docker.

## Develop

### Install python 3

This demo need python 3, follow this [guide](http://docs.python-guide.org/en/latest/starting/installation/) to install the latest python 3 to your system.

### Install pipenv

This demo use [pipenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) to manage dependencies.

```
$ pip install --user pipenv
```

### Clone repository

```
$ git clone git@github.com:jaggerwang/jw-tornado-demo.git
$ cd jw-tornado-demo
```

### Install dependencies

Install dependencies specified in the Pipfile.

```
$ pipenv sync
```

### Run

Run app in virtual env created by pipenv.

```
$ pipenv run python -m jwtornadodemo.app
```

Or activate virtual env first and run.

```
$ pipenv shell
$ python -m jwtornadodemo.app
```

It must to use `-m` to run the app module, because the app module used releative import.

You should change the default env values in module `jwtornadodemo.config.env` to your own, or change the default env values in command line, such as `PATH_DATA=/tmp MONGODB_HOST=localhost MONGODB_PORT=27017 pipenv run python -m jwtornadodemo.app`.

### Unit test

```
$ pipenv run python -m unittest
```

### Api test

```
$ curl http://localhost:8888/isLogined
{
    "code": 0,
    "message": ""
}
```

For full api list, check the app module.

## Deploy

### Install docker

Follow the official [instruction](https://docs.docker.com/install/) to install docker to your system.

### Clone repository

```
$ git clone git@github.com:jaggerwang/jw-tornado-demo.git
$ cd jw-tornado-demo
```

### Build image

Use `docker build` command to build app image, it use the Dockerfile located in the root directory of the demo project.

```
$ docker build -t jaggerwang.net/jw-tornado-demo .
```

You can change the tag name `jaggerwang.net/jw-tornado-demo` to whatever you want, but it must be the same with the image name in the following `docker-compose.yml` file.

`Dockerfile`

```
FROM python:3

ENV APP_PATH=/app
ENV DATA_PATH=/data

WORKDIR $APP_PATH

COPY ./Pipfile* ./
RUN pip install pipenv
RUN pipenv sync

COPY . .

VOLUME $DATA_PATH

EXPOSE 8888

CMD pipenv run python -m jwtornadodemo.app

```

### Run image

Use `docker-compose up` command to run app image and it's dependency images, including mongodb and redis.

```
$ docker-compose up
```

Your should modify `docker-compose.yml` as your own need, such as the app service's image name and all services's volume path.

`docker-compose.yml`

```
version: "2"
services:
  app:
    image: jaggerwang.net/jw-tornado-demo:latest
    environment:
      DEBUG: 'false'
      PATH_APP: /app
      PATH_DATA: /data
      LOGGING_LOGGER_LEVEL: INFO
      TORNADO_SERVER_PORT: 8888
      TORNADO_SERVER_NUMPROCS: 0
      SESSION_COOKIE_SECRET: 385aH8CvtcP51v985E56OgQryoIpzr61
      SESSION_EXPIRES_SECONDS: 86400
      MONGODB_HOST: mongodb
      MONGODB_PORT: 27017
      MONGODB_NAME: jw_tornado_demo
      REDIS_HOST: redis
      REDIS_PORT: 6379
      REDIS_DB: 0
    ports:
    - 19900:8888
    volumes:
    - ~/data/jw-tornado-demo/app:/data
  mongodb:
    image: mongo:3
    volumes:
    - ~/data/jw-tornado-demo/mongodb:/data/db
  redis:
    image: redis:4
    command:
    - redis-server
    - --appendonly
    - 'yes'
    volumes:
    - ~/data/jw-tornado-demo/redis:/data
```

### Other references

* [天火的技术博客](https://blog.jaggerwang.net/)
