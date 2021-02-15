# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      process server request
# Author:           tjq
# Created:          2021/2/15
# ------------------------------------------------------------------
import json
import tornado.ioloop
import tornado.web

from common.log import log
from common.constant import WORKER_RECEIVE_SCHEDULE_PATH


class ServerScheduleJobReq(object):

    def __init__(self, data=None):
        self.allWorkerAddress = []
        self.jobId = None
        self.wfInstanceId = None
        self.instanceId = None
        self.executeType = None
        self.processorType = None
        self.processorInfo = None
        self.instanceTimeoutMS = None
        self.jobParams = None
        self.instanceParams = None
        self.threadConcurrency = None
        self.taskRetryNum = None
        self.timeExpressionType = None
        self.timeExpression = None
        self.maxInstanceNum = None

        if data is not None:
            self.__dict__ = data


class ServerStopInstanceReq(object):

    def __init__(self, data=None):
        self.instanceId = None

        if data is not None:
            self.__dict__ = data


class ServerScheduleJobHandler(tornado.web.RequestHandler):

    def post(self):
        post_data = self.request.body.decode('utf-8')
        req = json.loads(post_data, object_hook=ServerScheduleJobReq)
        print(req)


class ServerRequestHandler(object):

    def __init__(self):
        self.application = tornado.web.Application([
            (WORKER_RECEIVE_SCHEDULE_PATH, ServerScheduleJobHandler),
        ])

    def start(self, ip, port):
        self.application.listen(port, ip)
        tornado.ioloop.IOLoop.instance().start()
