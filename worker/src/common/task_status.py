# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      TaskStatus
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
from enum import Enum


class TaskStatus(Enum):
    WAITING_DISPATCH = 1
    DISPATCH_SUCCESS_WORKER_UNCHECK = 2
    WORKER_RECEIVED = 3
    WORKER_PROCESSING = 4
    WORKER_PROCESS_FAILED = 5
    WORKER_PROCESS_SUCCESS = 6
