import json

import redis

from .. import config
from . import vo


class Cache(redis.StrictRedis):

    def __init__(self):
        super().__init__(**config.REDIS)

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
        return self.set(key, json.dumps(value, cls=vo.Encoder))

    def setex_json(self, key, expires, value):
        return self.setex(key, expires,
                          json.dumps(value, cls=vo.Encoder))

    def get_json(self, key, default=None):
        v = self.get(key)
        return (json.loads(v.decode(), cls=vo.Decoder)
                if v is not None else default)

    def get_json_pipe(self, keys, default=None):
        with self.pipeline() as pipe:
            for key in keys:
                pipe.get(key)
            values = pipe.execute()

        return [(json.loads(v.decode(), cls=vo.Decoder)
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
        return self.hset(key, field, json.dumps(value, cls=vo.Encoder))

    def hget_json(self, key, field, default=None):
        v = self.hget(key, field)
        return (json.loads(v.decode(), cls=vo.Decoder)
                if v is not None else default)

    def hmset_json(self, key, value):
        return self.hmget(key, {k: json.dumps(v, cls=vo.Encoder)
                                for k, v in value.items()})

    def hgetall_json(self, key):
        return {k.decode(): json.loads(v.decode(), cls=vo.Decoder)
                for k, v in self.hgetall(key).items()}

    def lpush_json(self, key, *values):
        if not values:
            return 0

        return self.lpush(key, *[json.dumps(v, cls=vo.Encoder)
                                 for v in values])

    def rpush_json(self, key, *values):
        if not values:
            return 0

        return self.rpush(key, *[json.dumps(v, cls=vo.Encoder)
                                 for v in values])

    def brpop_json(self, key, timeout=0):

        return json.dumps(self.brpop(key, timeout), cls=vo.Encoder)

    def lrange_json(self, key, start, stop):
        values = self.lrange(key, start, stop)
        return [json.loads(v.decode(), cls=vo.Decoder) for v in values]

    def lindex_json(self, key, index, default=None):
        v = self.lindex(key, index)
        return (json.loads(v.decode(), cls=vo.Decoder)
                if v is not None else default)

    def sadd_json(self, key, *values):
        if not values:
            return 0

        return self.sadd(key, *[json.dumps(v, cls=vo.Encoder)
                                for v in values])

    def srem_json(self, key, *values):
        if not values:
            return 0

        return self.srem(key, *[json.dumps(v, cls=vo.Encoder)
                                for v in values])

    def srandmember_str(self, key, limit=None):
        values = self.srandmember(key, limit)
        if limit is None:
            return values.decode() if values else None
        else:
            return [v.decode() for v in values]

    def srandmember_json(self, key, limit=None):
        values = self.srandmember(key, limit)
        if limit is None:
            return json.loads(values.decode(), cls=vo.Decoder)
        else:
            return [json.loads(v.decode(), cls=vo.Decoder)
                    for v in values]

    def zadd_json(self, key, *args, **kwargs):
        args = list(args)
        for i, v in enumerate(args):
            if i % 2 == 1:
                args[i] = json.dumps(v, cls=vo.Encoder)

        n_kwargs = {}
        for k, v in kwargs.items():
            n_kwargs[k] = json.dumps(v, cls=vo.Encoder)
        return self.zadd(key, *args, **n_kwargs)

    def zrevrange_json(self, key, start, stop, withscores=False,
                       score_cast_func=float):
        values = self.zrevrange(key, start, stop, withscores=withscores,
                                score_cast_func=score_cast_func)
        return [json.loads(v.decode(), cls=vo.Decoder) for v in values]

    def zrange_json(self, key, start, stop, withscores=False,
                    score_cast_func=float):
        values = self.zrange(key, start, stop, withscores=withscores,
                             score_cast_func=score_cast_func)
        return [json.loads(v.decode(), cls=vo.Decoder) for v in values]
