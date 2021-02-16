# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      remote test
# Author:           tjq
# Created:          2021/2/15
# ------------------------------------------------------------------
import time
from unittest import TestCase
from boot.worker_config import WorkerConfig
from boot.worker_meta import WorkerRuntimeMeta
from remote.handler.handler_starter import HttpHandlerStarter
from remote.heartbeat import HeartbeatSender
from remote.discovery import ServerDiscovery


cfg = WorkerConfig('py_client', ['127.0.0.1:7710', '127.0.0.1:7700'])
meta = WorkerRuntimeMeta()
meta.config = cfg
meta.localIp = '127.0.0.1'
meta.appId = 2
meta.workerAddress = '127.0.0.1:28888'
meta.currentServerAddress = '127.0.0.1:10010'


class TestRemote(TestCase):

    def test_http_handler_starer(self):
        HttpHandlerStarter().start('127.0.0.1', 28888)
        time.sleep(1000)

    def test_heartbeat(self):
        HeartbeatSender(meta).start()
        time.sleep(100)

    def test_discovery(self):
        ServerDiscovery(meta).start()
        time.sleep(100)
