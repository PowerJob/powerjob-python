# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      xxx
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
from unittest import TestCase
from worker.src.worker import Worker
from worker.src.worker import WorkerConfig


class TestWorker(TestCase):

    cfg = WorkerConfig('py_client', ['127.0.0.1:7700', '127.0.0.1:7700'])
    worker = Worker()
    worker.set_config(cfg)

    def test_init(self):
        TestWorker.worker.init()
