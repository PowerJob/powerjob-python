# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      WorkerRuntimeMeta
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
from boot.worker_config import WorkerConfig


class WorkerRuntimeMeta(object):

    def __init__(self):
        self.config: WorkerConfig = WorkerConfig('', [])
        self.appId = None
        self.workerAddress = None
        self.currentServerAddress = None
        self.localIp = None
