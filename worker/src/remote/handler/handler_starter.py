# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      start http server for handler
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
import tornado.ioloop
import tornado.web

from common.log import log
from common.constant import *
from remote.handler.server_request_handler import ServerScheduleJobHandler


class HttpHandlerStarter(object):

    def __init__(self):
        self.application = tornado.web.Application([
            (WORKER_RECEIVE_SCHEDULE_PATH, ServerScheduleJobHandler),
        ])

    def start(self, ip: str, port: int):
        log.info("[HttpHandler] start to listen %s:%d", ip, port)
        self.application.listen(port, ip)
        tornado.ioloop.IOLoop.instance().start()
