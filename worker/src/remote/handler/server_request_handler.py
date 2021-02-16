# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      process server request
# Author:           tjq
# Created:          2021/2/15
# ------------------------------------------------------------------
import json
from aiohttp import web
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


class ServerRequestHandler(object):

    async def on_receive_server_schedule_job_req(self, request: web.Request):
        data = await request.json()
        req = ServerScheduleJobReq(data)
        print(data)
        return web.Response(text='success')