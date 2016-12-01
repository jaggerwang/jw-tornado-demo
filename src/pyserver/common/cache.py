from json import dumps, loads

from redis import StrictRedis, ConnectionPool

from pyserver.config.cache import REDIS
from pyserver.common.vo import PyserverEncoder, PyserverDecoder


_connection_pools = {}


def get_connection_pool(alias):
    if alias not in _connection_pools:
        _connection_pools[alias] = ConnectionPool(**REDIS[alias])
    return _connection_pools[alias]


def get_redis(alias):
    return StrictRedis(connection_pool=get_connection_pool(alias))


class PyserverCache(StrictRedis):

    def __init__(self, alias):
        super().__init__(connection_pool=get_connection_pool(alias))

    def get_str(self, key, default=None):
        v = self.get(key)
        if isinstance(v, bytes):
            return v.decode()
        elif isinstance(v, int):
            return str(v)
        elif v is None:
            return default
        else:
            return v

    def get_int(self, key, default=None):
        v = self.get(key)
        return int(v) if v is not None else default

    def get_float(self, key, default=None):
        v = self.get(key)
        return float(v) if v is not None else default

    def set_json(self, key, value):
        return self.set(key, dumps(value, cls=PyserverEncoder))

    def setex_json(self, key, expires, value):
        return self.setex(key, expires, dumps(value, cls=PyserverEncoder))

    def get_json(self, key, default=None):
        v = self.get(key)
        return (loads(v.decode(), cls=PyserverDecoder)
                if v is not None else default)

    def get_json_pipe(self, keys, default=None):
        with self.pipeline() as pipe:
            for key in keys:
                pipe.get(key)
            values = pipe.execute()

        return [(loads(v.decode(), cls=PyserverDecoder)
                 if v is not None else default) for v in values]

    def hgetall_int(self, key):
        return {k.decode(): int(v) for k, v in self.hgetall(key).items()}

    def hgetall_int_pipe(self, keys):
        with self.pipeline() as pipe:
            for key in keys:
                pipe.hgetall(key)
            values = pipe.execute()

        return [{k1.decode(): int(v1) for k1, v1 in v.items()} for v in values]

    def hgetall_float(self, key):
        return {k.decode(): float(v) for k, v in self.hgetall(key).items()}

    def hgetall_float_pipe(self, keys):
        with self.pipeline() as pipe:
            for key in keys:
                pipe.hgetall(key)
            values = pipe.execute()

        return [{k1.decode(): float(v1) for k1, v1 in v.items()}
                for v in values]

    def hgetall_number(self, key):
        return {k.decode(): float(v) if '.' in v.decode() else int(v)
                for k, v in self.hgetall(key).items()}

    def hgetall_number_pipe(self, keys):
        with self.pipeline() as pipe:
            for key in keys:
                pipe.hgetall(key)
            values = pipe.execute()

        return [{k1.decode(): float(v1) if '.' in v1.decode() else int(v1)
                 for k1, v1 in v.items()}
                for v in values]

    def hset_json(self, key, field, value):
        return self.hset(key, field, dumps(value, cls=PyserverEncoder))

    def hget_json(self, key, field, default=None):
        v = self.hget(key, field)
        return (loads(v.decode(), cls=PyserverDecoder)
                if v is not None else default)

    def hmset_json(self, key, value):
        return self.hmget(key, {k: dumps(v, cls=PyserverEncoder)
                                for k, v in value.items()})

    def hgetall_json(self, key):
        return {k.decode(): loads(v.decode(), cls=PyserverDecoder)
                for k, v in self.hgetall(key).items()}

    def lpush_json(self, key, *values):
        if not values:
            return 0

        return self.lpush(key, *[dumps(v, cls=PyserverEncoder) for v in values])

    def rpush_json(self, key, *values):
        if not values:
            return 0

        return self.rpush(key, *[dumps(v, cls=PyserverEncoder) for v in values])

    def brpop_json(self, key, timeout=0):

        return dumps(self.brpop(key, timeout), cls=PyserverEncoder)

    def lrange_json(self, key, start, stop):
        values = self.lrange(key, start, stop)
        return [loads(v.decode(), cls=PyserverDecoder) for v in values]

    def lindex_json(self, key, index, default=None):
        v = self.lindex(key, index)
        return (loads(v.decode(), cls=PyserverDecoder)
                if v is not None else default)

    def sadd_json(self, key, *values):
        if not values:
            return 0

        return self.sadd(key, *[dumps(v, cls=PyserverEncoder) for v in values])

    def srem_json(self, key, *values):
        if not values:
            return 0

        return self.srem(key, *[dumps(v, cls=PyserverEncoder) for v in values])

    def srandmember_str(self, key, limit=None):
        values = self.srandmember(key, limit)
        if limit is None:
            return values.decode() if values else None
        else:
            return [v.decode() for v in values]

    def srandmember_json(self, key, limit=None):
        values = self.srandmember(key, limit)
        if limit is None:
            return loads(values.decode(), cls=PyserverDecoder)
        else:
            return [loads(v.decode(), cls=PyserverDecoder) for v in values]

    def zadd_json(self, key, *args, **kwargs):
        args = list(args)
        for i, v in enumerate(args):
            if i % 2 == 1:
                args[i] = dumps(v, cls=PyserverEncoder)

        n_kwargs = {}
        for k, v in kwargs.items():
            n_kwargs[k] = dumps(v, cls=PyserverEncoder)
        return self.zadd(key, *args, **n_kwargs)

    def zrevrange_json(self, key, start, stop, withscores=False,
                       score_cast_func=float):
        values = self.zrevrange(key, start, stop, withscores=withscores,
                                score_cast_func=score_cast_func)
        return [loads(v.decode(), cls=PyserverDecoder) for v in values]

    def zrange_json(self, key, start, stop, withscores=False,
                    score_cast_func=float):
        values = self.zrange(key, start, stop, withscores=withscores,
                             score_cast_func=score_cast_func)
        return [loads(v.decode(), cls=PyserverDecoder) for v in values]
