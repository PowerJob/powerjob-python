# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      remote test
# Author:           tjq
# Created:          2021/2/15
# ------------------------------------------------------------------
from unittest import TestCase
from worker.src.remote.heartbeat import HeartbeatSender


class TestRemote(TestCase):

    def test_heartbeat(self):
        sender = HeartbeatSender(2, 'py_client', '192.168.1.1:2345')
        sender.send('127.0.0.1:10010')
