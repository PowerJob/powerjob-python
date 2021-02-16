# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      process server request
# Author:           tjq
# Created:          2021/2/15
# ------------------------------------------------------------------
from aiohttp import web
from common.log import log
from remote.module.server_schedule_job_req import ServerScheduleJobReq
from remote.module.server_stop_instance_req import ServerStopInstanceReq


class ServerRequestHandler(object):

    async def on_receive_server_schedule_job_req(self, request: web.Request):
        data = await request.json()
        req = ServerScheduleJobReq(data)
        print(data)
        return web.Response(text='success')

    async def on_receive_server_stop_instance_req(self, request: web.Request):
        data = await request.json()
        req = ServerStopInstanceReq(data)
        print(data)
        return web.Response(text='success')
