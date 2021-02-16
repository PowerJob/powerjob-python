import requests
from common.constant import ASSERT_APP_URL
from common.log import log
from common.result import convert
from common.netutils import NetUtils
from common.exception import PowerJobError
from remote.heartbeat import HeartbeatSender
from remote.discovery import ServerDiscovery
from remote.handler.handler_starter import HttpHandlerStarter
from boot.worker_config import WorkerConfig
from boot.worker_meta import WorkerRuntimeMeta


class Worker(object):

    def __init__(self, cfg: WorkerConfig):
        self.meta = WorkerRuntimeMeta()

        self.meta.config = cfg
        self.meta.appId = None
        self.meta.workerAddress = None
        self.meta.currentServerAddress = None
        self.meta.localIp = None

    def init(self):
        self.meta.appId = self.assert_app_name()
        self.meta.localIp = NetUtils.get_local_host()
        self.meta.workerAddress = self.meta.localIp + ':' + str(self.meta.config.port)
        log.info("[Initialize] worker listen address: %s", self.meta.workerAddress)

        discovery = ServerDiscovery(self.meta)
        discovery.discovery()

        HttpHandlerStarter().start(self.meta.localIp, self.meta.config.port)
        HeartbeatSender(self.meta).start()
        discovery.start()

    def assert_app_name(self) -> int:
        app = self.meta.config.appName
        for address in self.meta.config.serverAddress:
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
            except IOError:
                log.warning("[Initialize] request failed, please check server address[%s]", address)
        raise PowerJobError('no server available')


