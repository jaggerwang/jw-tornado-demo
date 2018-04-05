import json
import logging
import re
import traceback
from datetime import datetime

import torndsession.sessionhandler

from . import error as err
from . import cache, vo
from .. import config


class Handler(torndsession.sessionhandler.SessionBaseHandler):

    def prepare(self):
        super().prepare()

        logger = logging.getLogger('app')
        logger.debug('{} {} {} {}'.format(
            self.request.method, self.request.path,
            self.request.arguments, self.request.headers))

    def get_current_user(self):
        return self.session['user']

    def write_error(self, status_code, **kwargs):
        if self.settings.get('serve_traceback') and 'exc_info' in kwargs:
            message = traceback.format_exception(*kwargs['exc_info'])
        else:
            message = self._reason
        error = err.Error(message)

        return self.response_json(error, status_code)

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
