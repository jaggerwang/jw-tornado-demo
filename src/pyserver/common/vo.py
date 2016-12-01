from datetime import datetime, date, timezone
from json import JSONEncoder, JSONDecoder
from importlib import import_module
from collections import OrderedDict

from bson import ObjectId


class PyserverVO(object):

    def __init__(self, mo, **kwargs):
        if kwargs and mo is not None:
            mo = dict(mo, **kwargs)

        self.mo = mo

    def __call__(self, handler):
        return self._copy_mo(handler)

    def __setitem__(self, key, value):
        if self.mo is not None:
            self.mo[key] = value

    def __getitem__(self, key, default=None):
        return self.mo.get(key, default) if self.mo else default

    def __contains__(self, key):
        return key in self.mo if self.mo else False

    def _copy_mo(self, handler, include=None, exclude=None):
        if self.mo is None:
            return None

        fields = (set(include or self.mo.keys()) - set(exclude or []))
        vo = {(k if k != '_id' else 'id'): v for k, v in self.mo.items()
              if k in fields}

        return jsonable(vo)


def jsonable(data, reserve_none=False):
    if (isinstance(data, list) or isinstance(data, tuple) or isinstance(
            data, set)):
        return [jsonable(v) for v in data
                if v is not None or reserve_none]
    elif isinstance(data, dict):
        if isinstance(data, OrderedDict):
            return jsonable(list(data.items()))
        else:
            return {jsonable(k): jsonable(v)
                    for k, v in data.items()
                    if v is not None or reserve_none}
    elif isinstance(data, datetime):
        return data.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(data, date):
        return data.strftime("%Y-%m-%d")
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data


class PyserverEncoder(JSONEncoder):

    def encode(self, o):
        return super().encode(encode_vo(o))


def encode_vo(o):
    if isinstance(o, PyserverVO):
        return {
            '$vo:v1:{}:{}'.format(
                o.__class__.__module__, o.__class__.__name__):
            encode_vo(o.mo)
        }
    elif isinstance(o, datetime):
        return {'$date': o.timestamp()}
    elif isinstance(o, ObjectId):
        return {'$oid': str(o)}
    elif isinstance(o, list) or isinstance(o, tuple) or isinstance(o, set):
        return [encode_vo(v) for v in o]
    elif isinstance(o, dict):
        return {k: encode_vo(v) for k, v in o.items()}
    else:
        return o


class PyserverDecoder(JSONDecoder):

    def decode(self, s):
        return decode_vo(super().decode(s))


def decode_vo(o, tz=timezone.utc):
    if isinstance(o, list):
        return [decode_vo(v, tz=tz) for v in o]
    elif isinstance(o, dict):
        if len(o) == 1:
            k, v = list(o.items())[0]
            if isinstance(k, str) and k.startswith('$vo:'):
                _, _, module, cls = k.split(':')
                cls = getattr(import_module(module), cls.replace('VOV2', 'VO'))
                o = cls.__new__(cls)
                o.mo = decode_vo(v, tz=tz)
                return o
            elif isinstance(k, str) and k == '$date':
                return datetime.fromtimestamp(v, tz=tz)
            elif isinstance(k, str) and k == '$oid':
                return ObjectId(v)
        return {k: decode_vo(v, tz=tz) for k, v in o.items()}
    else:
        return o
