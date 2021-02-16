# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      send heartbeat to server
# Author:           tjq
# Created:          2021/2/15
# ------------------------------------------------------------------
import os
import time
import multiprocessing
import json
import requests
import threading
from common.constant import HEARTBEAT_URL
from boot.worker_meta import WorkerRuntimeMeta


class SystemMetrics(object):

    def __init__(self):
        # cpu
        self.cpuProcessors = multiprocessing.cpu_count()
        self.cpuLoad = None

        # memory TODO：collect cpu load and memory info, then calculate the score
        self.jvmUsedMemory = None
        self.jvmMaxMemory = None
        self.jvmMemoryUsage = None

        # disk
        disk_info = os.statvfs('/')
        total_size = disk_info.f_blocks * disk_info.f_bsize / 1024 / 1024 / 1024
        free_size = disk_info.f_bsize * disk_info.f_bavail / 1024 / 1024 / 1024
        self.diskUsed = total_size - free_size
        self.diskTotal = total_size
        self.diskUsage = round(free_size / total_size * 100, 2)

        # need to calculate by worker
        self.score = 1


class WorkerHeartbeat(object):

    def __init__(self, worker_address, app_id, app_name):
        self.workerAddress = worker_address
        self.appName = app_name
        self.appId = app_id
        self.heartbeatTime = int(round(time.time() * 1000))
        self.protocol = 'HTTP'
        self.client = '5T5'
        self.systemMetrics = SystemMetrics().__dict__


class HeartbeatSender(object):

    def __init__(self, worker_runtime_meta: WorkerRuntimeMeta):
        self.meta = worker_runtime_meta

    def send(self):
        url = HEARTBEAT_URL % self.meta.currentServerAddress
        heartbeat = WorkerHeartbeat(self.meta.workerAddress, self.meta.appId, self.meta.config.appName)
        requests.post(url, data=json.dumps(heartbeat.__dict__))

    def start(self):

        def timing():
            while True:
                self.send()
                time.sleep(15)

        threading.Thread(target=timing(), name='power-heartbeat').start()

