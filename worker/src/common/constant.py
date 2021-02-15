WORKER_HTTP_PORT = 28888

# server path
ASSERT_APP_URL = 'http://%s/server/assert?appName=%s'
SERVER_DISCOVERY_URL = "http://%s/server/acquire?appId=%d&currentServer=%s&protocol=HTTP"

HEARTBEAT_URL = 'http://%s/server/heartbeat'
INSTANCE_STATUS_REPORT_URL = 'http://%s/server/heartbeat'
LOG_REPORT_URL = 'http://%s/server/logReport'


# worker path
WORKER_RECEIVE_SCHEDULE_PATH = r'/worker/runJob'
