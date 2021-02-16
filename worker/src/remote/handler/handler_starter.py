# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      start http server for handler
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
import tornado.web
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

from common.log import log
from common.constant import *
from remote.handler.server_request_handler import ServerScheduleJobHandler, ServerStopInstanceHandler


class HttpHandlerStarter(object):

    def __init__(self):
        self.app = tornado.web.Application([
            (WORKER_RECEIVE_SCHEDULE_PATH, ServerScheduleJobHandler),
            (WORKER_STOP_INSTANCE_PATH, ServerStopInstanceHandler),
        ])

    def start(self, ip: str, port: int):
        log.info("[HttpHandler] start to listen %s:%d", ip, port)
        server = HTTPServer(self.app)
        server.bind(port, ip)
        # Forks multiple sub-processes
        server.start(0)
        IOLoop.current().start()
        log.info("[HttpHandler] start tornado http server successfully!")
