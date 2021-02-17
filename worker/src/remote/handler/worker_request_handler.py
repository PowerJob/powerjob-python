# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      process worker request
# Author:           tjq
# Created:          2021/2/17
# ------------------------------------------------------------------
from aiohttp import web
from common.log import log
from persistence.task_do import TaskDO
from core.processor_tracker import ProcessorTracker
from core.pool import TaskTrackerPool, ProcessorTrackerPool
from remote.module.worker import TaskTrackerStartTaskReq, TaskTrackerStopInstanceReq


class WorkerRequestHandler(object):

    async def on_receive_task_tracker_start_task_req(self, request: web.Request):
        data = await request.json()
        req = TaskTrackerStartTaskReq(data)
        instance_id = req.instanceInfo.instanceId

        def creator():
            return TaskTrackerStartTaskReq(req)

        pt = ProcessorTrackerPool.get_processor_tracker(instance_id, req.taskTrackerAddress, creator())

        task = TaskDO()
        task.taskId = req.taskId
        task.taskName = req.taskName
        task.taskContent = req.taskContent
        task.failedCnt = req.taskCurrentRetryNums
        task.subInstanceId = req.subInstanceId

        pt.submit_task(task)

        return web.Response(text='success')

    async def on_receive_task_tracker_stop_instance_req(self, request: web.Request):
        data = await request.json()
        req = TaskTrackerStopInstanceReq(data)
        pts = ProcessorTrackerPool.remove(req.instanceId)
        for pt in pts:
            pt.destroy()

        return web.Response(text='success')


