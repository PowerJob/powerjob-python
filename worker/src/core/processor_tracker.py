# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      ProcessorTracker
# Author:           tjq
# Created:          2021/2/17
# ------------------------------------------------------------------
from persistence.task_do import TaskDO
from remote.module.worker import TaskTrackerStartTaskReq


class ProcessorTracker(object):

    def __init__(self, req: TaskTrackerStartTaskReq):
        pass

    def submit_task(self, task: TaskDO):
        pass

    def destroy(self):
        pass