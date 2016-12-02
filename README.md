# Jw-pyserver

An api server demo, which write in python, and deploy by docker.

### How to deploy

**run in prod mode**

Of course you should install docker engine first.
```
> git clone git@github.com:jaggerwang/jw-pyserver.git && cd jw-pyserver
> ./deploy-prod.sh
```
The deploy script use docker-compose to run all needed containers, including server, mongodb and redis.  
The data and log of server, mongodb and redis will be saved at host's directory "/data/jw-pyserver", which mounted at container's path "/data". You can change the data dir to your own, but the same change should be made to docker-compose file.

**run in dev mode with auto detecting code changing**

```
> git clone git@github.com:jaggerwang/jw-pyserver.git && cd jw-pyserver
> ./deploy.sh
> ./fswatch.sh # fswatch command needed, you can use brew to install it on macOS
```
The data and log of server, mongodb and redis will be saved at host's directory "~/data/projects/jw-pyserver/server", which mounted at container's path "/data". You can change the data dir to your own, but the same change should be made to docker-compose file.

**build image of your own**

```
> git clone git@github.com:jaggerwang/jw-pyserver.git && cd jw-pyserver
> ./docker-build.sh
```

### API

The server container exposed port 8888, and it mapped to port 10500 of the host. The domain used by cookie is pyserver.dev(in dev mode) or pyserver.net(in prod mode), Which configured in file "src/pyserver/config/main.py". So you can use domain "http://pyserver.dev:10500" to access the following api in dev mode.

Path|Method|Description
----|------|-----------
/register|POST|Register account.
/login|GET|Login.
/isLogined|GET|Check whether logined.
/logout|GET|Logout.
/account/edit|POST|Edit account profile.
/account/info|GET|Get current account info.
/file/upload|POST|Upload file, saved on local disk.
/file/info|GET|Get uploaded file info by id.
/upload/a.jpg|GET|Access uploaded file. The path can be found in the response of file upload api.

### FAQ

**How to change image repository?**

> Search and replace all "daocloud.io/jaggerwang/jw-pyserver" to your own.

**How can I build the base images of this project, including python, mongodb and redis?**

> The dockerfiles of the base images can be found at "https://github.com/jaggerwang/jw-dockerfiles".

### Other resources

* [Jag的技术博客](https://jaggerwang.net/)
