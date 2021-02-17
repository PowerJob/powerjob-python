# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      process server request
# Author:           tjq
# Created:          2021/2/15
# ------------------------------------------------------------------
from aiohttp import web
from common.log import log
from remote.module.server import ServerScheduleJobReq, ServerStopInstanceReq
from core.pool import TaskTracker, TaskTrackerPool


class ServerRequestHandler(object):

    async def on_receive_server_schedule_job_req(self, request: web.Request):
        data = await request.json()
        req = ServerScheduleJobReq(data)



        TaskTrackerPool.atomic_create_task_tracker(req.instanceId, )


        return web.Response(text='success')

    async def on_receive_server_stop_instance_req(self, request: web.Request):
        data = await request.json()
        req = ServerStopInstanceReq(data)
        print(data)
        return web.Response(text='success')
