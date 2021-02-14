# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      timing handler
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
from concurrent.futures import ThreadPoolExecutor
import requests
from background.model.heartbeat import WorkerHeartbeat


def timing_report_heartbeat():
    heartbeat = WorkerHeartbeat()
    requests.post()
