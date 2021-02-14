# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      heartbeat to server
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
import time
from background.model.metrics import SystemMetrics


class WorkerHeartbeat(object):

    def __init__(self, worker_address, app_id, app_name):
        self.workerAddress = worker_address
        self.appName =app_name
        self.appId = app_id
        self.heartbeatTime = int(round(time.time() * 1000))
        self.protocol = 'HTTP'
        self.client = '5T5'
        self.systemMetrics = SystemMetrics()
