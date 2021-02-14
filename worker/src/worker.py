import requests
from typing import List
from common.constant import *
from common.log import log
from common.exception import PowerJobError


class WorkerConfig(object):

    def __init__(self, app_name: str, server_address: List[str]):
        self.app_name = app_name
        self.server_address = server_address

        self.port = WORKER_HTTP_PORT
        self.max_result_length = 2048



class Worker(object):
    config: WorkerConfig = None
    appId: int = None
    address: str = None

    # I think this is a little bit java Style, but I like ~
    def set_config(self, cfg: WorkerConfig):
        self.config = cfg
        Worker.config = cfg

    def init(self):
        self.assert_app_name()


    def assert_app_name(self):
        app = self.config.app_name
        for address in self.config.server_address:
            url = ASSERT_APP_URL % (address, app)
            log.info("[PowerJobWorker] using url[%s] to assert app[%s]", url, app)
            try:
                res = requests.get(url).json()
                success = res['success']
                if success:
                    Worker.appId = res['data']
                    log.info("[PowerJobWorker] assert app[%s] successfully, appId is %d", app, Worker.appId)
                    return
                else:
                    log.error("[PowerJobWorker] assert app[%s] failed, please register first!", app)
                    raise PowerJobError(res['message'])
            except IOError as e:
                log.warn("[PowerJobWorker] request failed, please check server address[%s]", address, e)

    @staticmethod
    def get_worker_address() -> str:
        return Worker.address

    @staticmethod
    def get_current_app_name() -> str:
        return Worker.config.app_name

    @staticmethod
    def get_current_app_id() -> int:
        return Worker.appId
