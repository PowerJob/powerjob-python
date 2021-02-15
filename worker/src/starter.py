import requests
from typing import List
from common.constant import WORKER_HTTP_PORT, ASSERT_APP_URL, SERVER_DISCOVERY_URL
from common.log import log
from common.result import convert
from common.exception import PowerJobError


class WorkerConfig(object):

    def __init__(self, app_name: str, server_address: List[str]):
        self.app_name = app_name
        self.server_address = server_address

        self.port = WORKER_HTTP_PORT
        self.max_result_length = 2048


class Worker(object):

    def __init__(self, cfg: WorkerConfig):
        self.config = cfg
        self.appId = None
        self.worker_address = None
        self.server_address = None

    def init(self):
        self.appId = self.assert_app_name()
        self.worker_address = self.server_discovery()

    def assert_app_name(self) -> int:
        app = self.config.app_name
        for address in self.config.server_address:
            url = ASSERT_APP_URL % (address, app)
            log.info("[Initialize] using url[%s] to assert app[%s]", url, app)
            try:
                result = convert(requests.get(url).text)
                if result.success:
                    app_id = result.data
                    log.info("[Initialize] assert app[%s] successfully, appId is %d", app, app_id)
                    return app_id
                else:
                    log.error("[Initialize] assert app[%s] failed, please register first!", app)
                    raise PowerJobError(result.message)
            except IOError as e:
                log.warn("[Initialize] request failed, please check server address[%s]", address, e)
        raise PowerJobError('no server available')

    def server_discovery(self) -> str:
        for address in self.config.server_address:
            try:
                url = SERVER_DISCOVERY_URL % (address, self.appId, self.server_address)
                result = convert(requests.get(url).text)
                if result.success:
                    current_server_address = result.data
                    log.info("[Discovery] current server for app[%d] is: %s", self.appId, current_server_address)
                    return current_server_address
                else:
                    log.error("[Discovery] discovery server failed due to %s", result.message)
            except IOError as e:
                log.warn("[Discovery] discovery server failed due to request failed, address: %s", address, e)
        raise PowerJobError('no server available')
