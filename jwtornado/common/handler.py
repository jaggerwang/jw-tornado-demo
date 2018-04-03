import traceback
import re
import json
from datetime import datetime
import logging

import tornado.web

import pylib.session

from .. import config
from . import cache, error as err, vo


class Handler(tornado.web.RequestHandler):

    def prepare(self):
        super().prepare()

        logger = logging.getLogger('app')

        logger.debug('request: {}'.format(
            (self.request.method, self.request.path, self.request.arguments,
             dict(self.request.headers))))

    @property
    def session_store(self):
        if not hasattr(self, '_session_store'):
            self._session_store = pylib.session.RedisSessionStore(
                cache.Cache(),
                key_prefix=config.SESSION['key_prefix'],
                expires_days=config.SESSION['expires_days'])
        return self._session_store

    @property
    def sid(self):
        if not hasattr(self, '_sid'):
            sid = self.get_secure_cookie(config.SESSION['cookie_name'])
            sid = sid.decode() if sid else None
            if sid is None:
                sid = self.session_store.new_sid()
                self.set_secure_cookie(
                    config.SESSION['cookie_name'],
                    sid,
                    expires_days=config.SESSION['expires_days'])
            self._sid = sid
        return self._sid

    @property
    def session(self):
        if not hasattr(self, '_session'):
            logger = logging.getLogger('app')

            self._session = pylib.session.Session(self.session_store, self.sid)
            logger.debug('create session: {}'.format(self.sid))
        return self._session

    def get_current_user(self):
        return self.session['user']

    @property
    def current_user_id(self):
        return self.current_user['_id'] if self.current_user else None

    def response_json(self, error=None, status_code=200, **kwargs):
        data = {
            'code': err.ERROR_CODE_OK,
            'message': ''
        }
        if error:
            data['code'] = error.code
            data['message'] = (
                error.message if (config.DEBUG and error.message) else
                err.MESSAGES.get(error.code, '')
            )
        data.update(kwargs)

        ua = self.request.headers.get('User-Agent', '')
        if re.match(r'.+\s+MSIE\s+.+', ua):
            content_type = 'text/html; charset=utf-8'
        else:
            content_type = 'application/json; charset=utf-8'
        content = json.dumps(
            vo.jsonable(data),
            indent=(None if not config.DEBUG else 4),
            ensure_ascii=False)
        self.response(content, content_type, status_code)

    def response_html(self, template, error=None, status_code=200, **kwargs):
        data = {
            'code': err.ERROR_CODE_OK,
            'message': ''
        }
        if error:
            data['code'] = error.code
            data['message'] = (
                error.message if (config.DEBUG and error.message) else
                err.MESSAGES.get(error.code, '')
            )
        data.update(kwargs)

        content = self.render_string(template, **data)
        content_type = 'text/html; charset=utf-8'
        self.response(content, content_type, status_code)

    def response(self, content, content_type, status_code=200):
        self.set_status(status_code)
        self.set_header('Content-Type', content_type)
        self.finish(content)

    def write_error(self, status_code, **kwargs):
        if self.settings.get('serve_traceback') and 'exc_info' in kwargs:
            message = traceback.format_exception(*kwargs['exc_info'])
        else:
            message = self._reason
        error = err.Error(message)

        return self.response_json(error, status_code)

    def on_finish(self):
        rlogger = logging.getLogger('request')

        rlogger.info(json.dumps(vo.jsonable({
            'request_time': datetime.now(),
            'time_served': self.request.request_time(),
            'http_user_agent': self.request.headers.get('User-Agent', ''),
            'remote_ip': self.request.remote_ip,
            'method': self.request.method,
            'path': self.request.path,
            'arguments': {
                k.translate({
                    ord('.'): '_',
                    ord('\''): '_',
                    ord('"'): '_',
                }):
                v[0].decode(errors='replace')
                for k, v in self.request.arguments.items()
            },
            'current_user_id': self.current_user_id,
        })))
