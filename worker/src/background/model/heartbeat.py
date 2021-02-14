# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      heartbeat to server
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
import time
from background.model.metrics import SystemMetrics
from worker.src.worker import Worker


class WorkerHeartbeat(object):

    def __init__(self):
        self.workerAddress = Worker.get_worker_address()
        self.appName = Worker.get_current_app_name()
        self.appId = Worker.get_current_app_id()
        self.heartbeatTime = int(round(time.time() * 1000))
        self.protocol = 'HTTP'
        self.client = '5T5'
        self.systemMetrics = SystemMetrics()
