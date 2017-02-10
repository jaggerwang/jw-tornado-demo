#!/usr/bin/env python3
import os
import logging.config

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options
from tornado.web import Application, StaticFileHandler

from pyserver.config.main import *
from pyserver.config.log import LOGGING
from pyserver.account.handler import *

app = Application([
    (r"/static/(.*)", StaticFileHandler, {'path': STATIC_PATH}),

    (r"/register", RegisterUserHandler, None, "register"),
    (r"/login", LoginHandler, None, "login"),
    (r"/isLogined", isLoginedHandler),
    (r"/logout", LogoutHandler, None, "logout"),
    (r"/account/edit", EditUserHandler),
    (r"/account/info", AccountInfoHandler),
], **SETTINGS)

if __name__ == '__main__':
    define("port", default=8888, type=int,
           help="listen port")
    define("numprocs", default=0, type=int,
           help="number of subprocess to fork")
    options.logging = None
    parse_command_line()

    if not os.path.exists(UPLOAD_PATH):
        os.makedirs(UPLOAD_PATH)

    logging.config.dictConfig(LOGGING)

    server = HTTPServer(app, xheaders=True)
    if SETTINGS['debug']:
        server.listen(options.port)
    else:
        server.bind(options.port)
        server.start(options.numprocs)
    IOLoop.current().start()
