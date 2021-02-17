# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      request from server
# Author:           tjq
# Created:          2021/2/17
# ------------------------------------------------------------------


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