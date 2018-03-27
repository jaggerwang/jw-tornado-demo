# jw-api-server-tornado-demo

An python api server starter kit, deploy using docker.

### Packages

|Package|Description|
|-------|-----------|
|[tornado](https://github.com/tornadoweb/tornado)|Http server and framework.|
|[WTForms](https://github.com/wtforms/wtforms)|Validate form values.|
|[cement](https://github.com/datafolklabs/cement)|CLI app framework.|
|[requests](https://github.com/kennethreitz/requests)|Http request.|
|[pymongo](https://github.com/mongodb/mongo-python-driver)|Mongodb driver.|
|[redis](https://github.com/andymccurdy/redis-py)|Redis driver.|

### How to deploy

You need install [docker engine](https://docs.docker.com/engine/installation/) first.

**run in dev mode with auto detecting code changing**

```
> git clone git@github.com:jaggerwang/jw-api-server-tornado-demo.git && cd jw-api-server-tornado-demo
> mkdir -p ~/data/projects/jw-api-server-tornado-demo # create directory for data volumes
> ./deploy.sh # pull images and run containers
> ./fswatch.sh # watching code change, fswatch needed
```

The data and log of server, mongodb and redis will be saved at host's path "~/data/projects/jw-api-server-tornado-demo", which mounted at container's path "/data".

**run in prod mode**

```
> git clone git@github.com:jaggerwang/jw-api-server-tornado-demo.git && cd jw-api-server-tornado-demo
> mkdir -p /data/jw-api-server-tornado-demo # create directory for data volumes
> ./deploy-prod.sh
```

The data and log of server, mongodb and redis will be saved at host's path "/data/jw-api-server-tornado-demo", which mounted at container's path "/data".

**build image of your own**

```
> cd jw-api-server-tornado-demo
> ./docker-build.sh
```

### Command

**help**

```
> cd jw-api-server-tornado-demo
> docker-compose -p jw-api-server-tornado-demo exec server ./src/manage.py -h
usage: pyserver (sub-commands ...) [options ...] {arguments ...}

Pyserver admin console.

commands:

  create-mongodb-index
    Create mongodb index.

  default

  test
    Run unittest.

optional arguments:
  -h, --help  show this help message and exit
  --debug     toggle debug output
  --quiet     suppress all output
  -t, --test  init test environment
```

**create mongodb index**

```
> cd jw-api-server-tornado-demo
> docker-compose -p jw-api-server-tornado-demo exec server ./src/manage.py create-mongodb-index
```
When deploy, it will auto run this command to create mongodb index. So normally you do not need to do this by your own.

**run unittest**

```
> cd jw-api-server-tornado-demo
> docker-compose -p jw-api-server-tornado-demo exec server ./src/manage.py test
......
----------------------------------------------------------------------
Ran 6 tests in 0.036s

OK
```
The test will run on a new db on the same instance, it's name prefixed 'test\_' to the origin, and using redis cache db no 16.

### API

The server container exposed port 8888, and it mapped to port 10500 of the host. So you can use domain "http://localhost:10500" to access the following api.

Path|Method|Description
----|------|-----------
/register|POST|Register account.
/login|GET|Login.
/isLogined|GET|Check whether logined.
/logout|GET|Logout.
/account/edit|POST|Edit account profile.
/account/info|GET|Get current account info.

### FAQ

**How to change image repository?**

> Search and replace all "daocloud.io/jaggerwang/jw-api-server-tornado-demo" to your own.

**How can I build the base images of this project, including go, mongodb and redis?**

> The dockerfiles of the base images can be found at "https://github.com/jaggerwang/jw-dockerfiles".

### Other resources

* [Jag的技术博客](https://jaggerwang.net/)
