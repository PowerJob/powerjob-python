# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      server discovery
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
import time
import threading
import requests
from boot.worker_meta import WorkerRuntimeMeta
from common.log import log
from common.result import convert
from common.exception import PowerJobError
from common.constant import SERVER_DISCOVERY_URL


class ServerDiscovery(object):

    def __init__(self, worker_runtime_meta: WorkerRuntimeMeta):
        self.meta = worker_runtime_meta

    def discovery(self) -> str:
        for address in self.meta.config.serverAddress:
            try:
                url = SERVER_DISCOVERY_URL % (address, self.meta.appId, self.meta.currentServerAddress)
                result = convert(requests.get(url).text)
                if result.success:
                    current_server_address = result.data
                    log.info("[Discovery] current server for app[%d] is: %s", self.meta.appId, current_server_address)
                    return current_server_address
                else:
                    log.error("[Discovery] discovery server failed due to %s", result.message)
            except IOError:
                log.warning("[Discovery] request failed, using server address: %s", address, exc_info=True)
        raise PowerJobError('no server available')

    def start(self):

        def timing():
            while True:
                time.sleep(13)
                self.meta.currentServerAddress = self.discovery()

        threading.Thread(target=timing(), name='power-discovery').start()
