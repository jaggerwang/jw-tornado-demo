# Jw-pyserver

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
> git clone git@github.com:jaggerwang/jw-pyserver.git && cd jw-pyserver
> mkdir -p ~/data/projects/jw-pyserver # create directory for data volumes
> ./deploy.sh # pull images and run containers
> ./fswatch.sh # watching code change, fswatch needed
```

The data and log of server, mongodb and redis will be saved at host's path "~/data/projects/jw-pyserver", which mounted at container's path "/data".

**run in prod mode**

```
> git clone git@github.com:jaggerwang/jw-pyserver.git && cd jw-pyserver
> mkdir -p /data/jw-pyserver # create directory for data volumes
> ./deploy-prod.sh
```

The data and log of server, mongodb and redis will be saved at host's path "/data/jw-pyserver", which mounted at container's path "/data".

**build image of your own**

```
> cd jw-pyserver
> ./docker-build.sh
```

**create mongodb index**

```
> cd jw-pyserver
> docker-compose -p jw-pyserver exec server ./src/manage.py create-mongodb-index
```
When deploy, it will auto run this command to create mongodb index. So normally you do not need to do this by your own.

### API

The server container exposed port 1323, and it mapped to port 10400 of the host. So you can use domain "http://localhost:10400" to access the following api.

Path|Method|Description
----|------|-----------
/register|POST|Register account.
/login|GET|Login.
/isLogined|GET|Check whether logined.
/logout|GET|Logout.
/account/edit|POST|Edit account profile.
/account/info|GET|Get current account info.
/user/info|GET|Get user info by id.
/user/infos|GET|Get user info by ids.

### FAQ

**How to change image repository?**

> Search and replace all "daocloud.io/jaggerwang/jw-pyserver" to your own.

**How can I build the base images of this project, including go, mongodb and redis?**

> The dockerfiles of the base images can be found at "https://github.com/jaggerwang/jw-dockerfiles".

### Other resources

* [Jag的技术博客](https://jaggerwang.net/)
