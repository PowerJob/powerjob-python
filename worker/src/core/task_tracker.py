# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      The master node for one job instance
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import List
from abc import ABCMeta, abstractmethod
from common.log import log
from common.lock import SegmentLock
from common.task_status import TaskStatus
from common.execute_type import ExecuteType
from common.constant import ROOT_TASK_NAME, LAST_TASK_NAME, EMPTY_ADDRESS, BROADCAST_TASK_NAME
from core.cluster import ProcessorTrackerStatusHolder
from persistence.task_do import TaskDO
from persistence.task_service import TaskService
from remote.module.server import ServerScheduleJobReq
from remote.module.worker import ProcessorTrackerStatusReportReq, TaskTrackerStopInstanceReq


class InstanceInfo(object):

    def __init__(self, req: ServerScheduleJobReq):
        self.jobId = req.jobId
        self.instanceId = req.instanceId
        self.wfInstanceId = req.wfInstanceId

        self.executeType = req.executeType
        self.processorType = req.processorType
        self.processorInfo = req.processorInfo
        self.timeExpressionType = req.timeExpressionType

        self.instanceTimeoutMS = req.instanceTimeoutMS
        self.jobParams = req.jobParams
        self.instanceParams = req.instanceParams

        self.threadConcurrency = max(req.threadConcurrency, 1)
        self.taskRetryNum = req.taskRetryNum

        # 处理非法参数
        if self.instanceTimeoutMS <= 0:
            self.instanceTimeoutMS = 24 * 3600 * 1000


class TaskTracker(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def init_task_tracker(self):
        pass

    def __init__(self, req: ServerScheduleJobReq):
        self.createTime = int(round(time.time() * 1000))
        self.instanceId = req.instanceId
        self.instanceInfo = InstanceInfo(req)

        self.ptStatusHolder = ProcessorTrackerStatusHolder(req.allWorkerAddress)
        self.taskPersistenceService = TaskService()
        self.finished = False

        self.taskId2LastReportTime = dict()
        # python 线程模型比较玄学，先并发度为 1 保证安全
        self.segmentLock = SegmentLock(1)

        # 调度线程池
        self.scheduledPool = ThreadPoolExecutor(max_workers=4, thread_name_prefix='PTS')

        self.init_task_tracker()

        log.info('[TaskTracker-%d] create TaskTracker successfully.', self.instanceId)

    def update_task_status(self, sub_instance_id, task_id, status, report_time, result):
        if self.finished:
            return
        n_task_status = TaskStatus(status)

        lock_id = hash(task_id)

        try:
            self.segmentLock.lock(lock_id)
            last_report_time = self.taskId2LastReportTime.get(task_id)
            if last_report_time is None:
                task = self.taskPersistenceService.get_task(self.instanceId, task_id)
                if task is not None:
                    last_report_time = task.lastReportTime
                else:
                    log.error("[TaskTracker-%d-%d] can't find task[id=%s]", self.instanceId, sub_instance_id, task_id)

            if last_report_time is None:
                last_report_time = -1

            # 过滤过期的请求（潜在的集群时间一致性需求，重试跨Worker时，时间不一致可能导致问题）
            if last_report_time > report_time:
                log.warning("[TaskTracker-%d-%d] received expired report: taskId=%s,status=%d,result=%s",
                            self.instanceId, sub_instance_id, task_id, status, result)
                return

            self.taskId2LastReportTime[task_id] = report_time

            config_task_retry_num = self.instanceInfo.taskRetryNum
            if n_task_status == TaskStatus.WORKER_PROCESS_FAILED and config_task_retry_num >= 1:
                task = self.taskPersistenceService.get_task(self.instanceId, task_id)
                if task is not None:
                    failed_cnt = task.failedCnt
                    if failed_cnt < config_task_retry_num:
                        update_entity = TaskDO()
                        update_entity.failedCnt = failed_cnt + 1

                        task_name = task.taskName
                        execute_type = ExecuteType[self.instanceInfo.executeType]
                        if task_name != ROOT_TASK_NAME and task_name != LAST_TASK_NAME and execute_type != ExecuteType.BROADCAST:
                            update_entity.address = EMPTY_ADDRESS

                        update_entity.status = TaskStatus.WAITING_DISPATCH.value
                        update_entity.lastReportTime = report_time

                        success = self.taskPersistenceService.update_task(self.instanceId, task_id, update_entity)
                        if success:
                            log.info("[TaskTracker-%d-%d] task(id=%s) process failed, TaskTracker will have a retry.",
                                     self.instanceId, sub_instance_id, task_id)
                            return

            if result is None:
                result = ''

            s = self.taskPersistenceService.update_task_status(self.instanceId, task_id, status, report_time, result)
            if not s:
                log.warning(
                    "[TaskTracker-%d-%d] update task status failed, this task(taskId=%s) may be processed repeatedly!",
                    self.instanceId, sub_instance_id, task_id)
        except RuntimeError:
            log.exception("[TaskTracker-%d-%d] update task status failed.", self.instanceId, sub_instance_id)
        finally:
            self.segmentLock.unlock(lock_id)

    def submit_task(self, tasks: List[TaskDO]) -> bool:
        if self.finished:
            return True
        if tasks is None or len(tasks) == 0:
            return True

        now = int(round(time.time() * 1000))
        for task in tasks:
            task.instanceId = self.instanceId
            task.status = TaskStatus.WAITING_DISPATCH.value
            task.failedCnt = 0
            task.lastModifiedTime = now
            task.createdTime = now
            task.lastReportTime = -1

        return self.taskPersistenceService.batch_save(tasks)

    def receive_processor_tracker_heartbeat(self, heartbeat: ProcessorTrackerStatusReportReq):
        self.ptStatusHolder.update(heartbeat.address, heartbeat.time, heartbeat.remainTaskNum)

        # 上报空闲，检查是否已经接收到全部该 ProcessorTracker 负责的任务
        if heartbeat.type == ProcessorTrackerStatusReportReq.IDLE:
            idle_pt_addr = heartbeat.address
            # 该 ProcessorTracker 已销毁，重置为初始状态
            self.ptStatusHolder.get_processor_tracker_status(idle_pt_addr).dispatched(False)
            unfinished = self.taskPersistenceService.get_all_unfinished_task_by_address(self.instanceId, idle_pt_addr)
            if unfinished is not None and len(unfinished) > 0:
                log.warning('[TaskTracker-%d] ProcessorTracker(%s) is idle now but have unfinished tasks: {}',
                            self.instanceId, idle_pt_addr, unfinished)
                for task in unfinished:
                    self.update_task_status(task.subInstanceId, task.taskId, TaskStatus.WORKER_PROCESS_FAILED.value,
                                            int(round(time.time() * 1000)), 'SYSTEM: unreceived process result')

    def broadcast(self, pre_execute_success: bool, sub_instance_id, pre_task_id, result):
        if self.finished:
            return
        log.info("[TaskTracker-%d-%d] finished broadcast's preProcess, preExecuteSuccess:%s,preTaskId:%s,result:%s",
                 self.instanceId, sub_instance_id, pre_execute_success, pre_task_id, result)

        if pre_execute_success:
            sub_tasks = list()
            for idx, address in self.ptStatusHolder.get_all_processor_tackers():
                one = TaskDO()
                one.subInstanceId = sub_instance_id
                one.taskName = BROADCAST_TASK_NAME
                one.taskId = pre_task_id + '.' + idx
                one.address = address
                sub_tasks.append(one)

            self.submit_task(sub_tasks)
        else:
            log.warn("[TaskTracker-%d-%d] BroadcastTask failed because of preProcess failed, preProcess result=%s.",
                     self.instanceId, sub_instance_id, result)

    def destroy(self):

        self.finished = True
        self.scheduledPool.shutdown(wait=False)

        # 通知 ProcessorTracker 释放资源  TODO: RELEASE DATA
        stop_request = TaskTrackerStopInstanceReq()
        stop_request.instanceId = self.instanceId











