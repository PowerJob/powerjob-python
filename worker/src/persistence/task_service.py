# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      TaskService
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
import time
import threading
from typing import List
from common.task_status import TaskStatus
from common.constant import EMPTY_ADDRESS, LAST_TASK_NAME
from persistence.task_do import TaskDO
from persistence.query import SimpleTaskQuery
from persistence.task_dao_impl import TaskDaoImpl
from core.processor import TaskResult


class TaskService(object):

    RETRY_TIMES = 3
    RETRY_INTERVAL_MS = 100

    _instance_lock = threading.Lock()

    # 高端单例
    def __new__(cls, *args, **kwargs):
        if not hasattr(TaskService, "_instance"):
            with TaskService._instance_lock:
                if not hasattr(TaskService, "_instance"):
                    TaskService._instance = object.__new__(cls)
        return TaskService._instance

    def __init__(self):
        self.taskDAO = TaskDaoImpl()

    def init(self):
        self.taskDAO.init_table()

    def save(self, task: TaskDO) -> bool:
        self.taskDAO.save(task)
        return True

    def batch_save(self, tasks: List[TaskDO]) -> bool:
        self.taskDAO.batch_save(tasks)
        return True

    def update_task(self, instance_id, task_id, entity: TaskDO):
        entity.lastModifiedTime = int(round(time.time() * 1000))
        query = TaskService.gen_key_query(instance_id, task_id)
        self.taskDAO.simple_update(query, entity)
        return True

    def update_task_status(self, instance_id, task_id, status, report_time, result):
        self.taskDAO.update_status(instance_id, task_id, status, report_time, result)

    def update_lost_tasks(self, instance_id, address_list: List[str], retry: bool):
        entity = TaskDO()
        entity.lastModifiedTime = int(round(time.time() * 1000))
        if retry:
            entity.address = EMPTY_ADDRESS
            entity.status = TaskStatus.WAITING_DISPATCH.value
        else:
            entity.status = TaskStatus.WORKER_PROCESS_FAILED.value
            entity.result = 'maybe worker down'

        address_in = TaskService.list2string(address_list)
        query_condition_format = 'address in %s and status not in (%d, %d)'
        query_condition = query_condition_format % (address_in, TaskStatus.WORKER_PROCESS_FAILED.value,
                                                    TaskStatus.WORKER_PROCESS_SUCCESS.value)

        query = SimpleTaskQuery()
        query.instanceId = instance_id
        query.queryCondition = query_condition

        self.taskDAO.simple_update(query, entity)
        return True

    def get_last_task(self, instance_id, sub_instance_id):
        query = SimpleTaskQuery()
        query.instanceId = instance_id
        query.subInstanceId = sub_instance_id
        query.taskName = LAST_TASK_NAME
        collection = self.taskDAO.simple_query(query)
        if collection is None or len(collection) == 0:
            return None
        return collection[0]

    def get_all_task(self, instance_id, sub_instance_id) -> List[TaskDO]:
        query = SimpleTaskQuery()
        query.instanceId = instance_id
        query.subInstanceId = sub_instance_id
        return self.taskDAO.simple_query(query)

    def get_all_unfinished_task_by_address(self, instance_id, address) -> List[TaskDO]:
        query = SimpleTaskQuery()
        query.instanceId = instance_id
        query.address = address
        query.queryCondition = 'status not in (%d, %d)' % (TaskStatus.WORKER_PROCESS_SUCCESS.value,
                                                           TaskStatus.WORKER_PROCESS_FAILED.value)

        return self.taskDAO.simple_query(query)

    def get_task_by_status(self, instance_id, status: TaskStatus, limit) -> List[TaskDO]:
        query = SimpleTaskQuery()
        query.instanceId = instance_id
        query.status = status.value
        query.limit = limit
        return self.taskDAO.simple_query(query)

    def get_task_status_statistics(self, instance_id, sub_instance_id) -> dict:
        query = SimpleTaskQuery()
        query.instanceId = instance_id
        query.subInstanceId = sub_instance_id
        query.queryContent = 'status, count(*) as num'
        query.otherCondition = 'GROUP BY status'

        db_result = self.taskDAO.simple_query_plus(query)
        result = dict()
        for row in db_result:
            status = int(row.get('status'))
            num = int(row.get('num'))
            result[status] = num
        return result

    def get_all_task_result(self, instance_id, sub_instance_id) -> List[TaskResult]:
        query = SimpleTaskQuery()
        query.instanceId = instance_id
        query.subInstanceId = sub_instance_id
        query.queryContent = 'status, result, task_id'

        db_result = self.taskDAO.simple_query_plus(query)
        result = list()
        for row in db_result:
            one = TaskResult()
            one.result = row.get('result')
            one.taskId = row.get('task_id')
            one.success = int(row.get('status')) == TaskStatus.WORKER_PROCESS_SUCCESS.value
            result.append(one)
        return result

    def get_task(self, instance_id, task_id):
        query = TaskService.gen_key_query(instance_id, task_id)
        res = self.taskDAO.simple_query(query)
        if res is None or len(res) == 0:
            return None
        return res[0]

    def delete_all_tasks(self, instance_id) -> bool:
        query = SimpleTaskQuery()
        query.instanceId = instance_id
        self.taskDAO.simple_delete(query)
        return True

    def delete_all_sub_instance_tasks(self, instance_id, sub_instance_id) -> bool:
        query = SimpleTaskQuery()
        query.instanceId = instance_id
        query.subInstanceId = sub_instance_id
        self.taskDAO.simple_delete(query)
        return True


    @staticmethod
    def gen_key_query(instance_id, task_id) -> SimpleTaskQuery:
        q = SimpleTaskQuery()
        q.instanceId = instance_id
        q.taskId = task_id
        return q

    @staticmethod
    def list2string(collection: List[str]) -> str:
        if collection is None or len(collection) == 0:
            return '()'
        res = ' ( '
        for one in collection:
            res = res + "'" + one + "',"
        return res[0: len(res) - 1] + ' ) '