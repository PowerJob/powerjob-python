# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      PowerJob Processor API
# Author:           tjq
# Created:          2021/2/15
# ------------------------------------------------------------------
from typing import List
from abc import ABCMeta, abstractmethod


class ProcessResult(object):

    def __init__(self, success=False, msg=None):
        self.success = success
        self.msg = msg


class TaskContext(object):

    def __init__(self):
        self.jobId = None
        self.instanceId = None
        self.subInstanceId = None
        self.taskId = None
        self.taskName = None
        self.jobParams = None
        self.instanceParams = None
        self.maxRetryTimes = None
        self.currentRetryTimes = None
        self.subTask = None

        self.omsLogger = None


class TaskResult(object):

    def __init__(self):
        self.taskId = None
        self.success = False
        self.result = None


class BasicProcessor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, context: TaskContext) -> ProcessResult:
        pass


class BroadcastProcessor(BasicProcessor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def pre_process(self, context: TaskContext) -> ProcessResult:
        pass

    def post_process(self, context: TaskContext, results: List[TaskResult]) -> ProcessResult:
        succeed = failed = 0
        for result in results:
            if result.success:
                succeed = succeed + 1
            else:
                failed = failed + 1
        process_result = ProcessResult()
        process_result.success = failed == 0
        process_result.msg = 'success: %d, failed: %d' % (succeed, failed)
        return process_result


class MapProcessor(BasicProcessor):
    __metaclass__ = ABCMeta

    def map(self, sub_task_list: List, sub_task_name: str) -> ProcessResult:
        # TODO: map
        pass


class MapReduceProcessor(MapProcessor):
    __metaclass__ = ABCMeta

    @abstractmethod
    def reduce(self, task: TaskContext, result_list: List[TaskResult]) -> ProcessResult:
        pass
