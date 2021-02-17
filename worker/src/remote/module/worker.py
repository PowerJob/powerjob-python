# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      request between worker
# Author:           tjq
# Created:          2021/2/17
# ------------------------------------------------------------------
from typing import List


class SubTask(object):

    def __init__(self):
        self.taskId = None
        self.taskContent = None


class ProcessorMapTaskRequest(object):
    def __init__(self):
        self.instanceId = None
        self.subInstanceId = None
        self.taskName = None
        self.subTasks: List[SubTask] = []


class ProcessorReportTaskStatusReq(object):

    BROADCAST = 1

    def __init__(self, data=None):
        self.instanceId = None
        self.subInstanceId = None
        self.taskId = None
        self.status = None
        self.result = None
        self.reportTime = None
        self.cmd = None

        if data is not None:
            self.__dict__ = data


class ProcessorTrackerStatusReportReq(object):

    IDLE = 1
    LOAD = 2

    def __init__(self, data=None):
        self.type = None
        self.instanceId = None
        self.time = None
        self.remainTaskNum = None
        self.address = None

        if data is not None:
            self.__dict__ = data


class TaskTrackerStartTaskReq(object):

    def __init__(self, data=None):
        self.taskTrackerAddress = None
        self.instanceInfo = None
        self.taskId = None
        self.taskName = None
        self.taskContent = None
        self.taskCurrentRetryNums = None
        self.subInstanceId = None

        if data is not None:
            self.__dict__ = data


class TaskTrackerStopInstanceReq(object):

    def __init__(self, data=None):
        self.instanceId = None
        self.type = None

        if data is not None:
            self.__dict__ = data
