# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      WorkerConfig
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
from typing import List
from common.constant import WORKER_HTTP_PORT, ASSERT_APP_URL, SERVER_DISCOVERY_URL, HEARTBEAT_URL


class WorkerConfig(object):

    def __init__(self, app_name: str, server_address: List[str]):
        self.appName = app_name
        self.serverAddress = server_address

        self.port = WORKER_HTTP_PORT
        self.maxResultLength = 2048
