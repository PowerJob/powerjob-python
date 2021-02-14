import logging
import common.constant
from typing import List


class WorkerConfig(object):

    def __init__(self, app_name: str, server_address: List[str]):
        self.app_name = app_name
        self.server_address = server_address

        self.port = common.constant.WORKER_HTTP_PORT
        self.max_result_length = 2048
        self.required = True


class Worker(object):
    config: WorkerConfig = None

    # I think this is a little bit java Style, but I like ~
    def set_config(self, cfg: WorkerConfig):
        self.config = cfg
        Worker.config = cfg


