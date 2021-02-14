# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      just for test
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
from unittest import TestCase
from persistence.task_dao_impl import TaskDaoImpl
from persistence.task_do import TaskDO
from persistence.query import SimpleTaskQuery

taskDaoImpl = TaskDaoImpl()


def task_generator(task_id: str, instance_id: int):
    task = TaskDO()
    task.taskId = task_id
    task.instanceId = instance_id
    task.subInstanceId = instance_id
    task.taskName = "test task"
    task.address = '192.168.1.1'
    task.status = 0
    task.failedCnt = 0
    task.createdTime = 1613286756173
    task.lastModifiedTime = 1613286756173
    task.lastReportTime = -1
    return task


class TestTaskDaoImpl(TestCase):

    def test_init_table(self):
        taskDaoImpl.init_table()

    def test_save(self):
        task = task_generator("0", 100)
        taskDaoImpl.save(task)

    def test_batch_save(self):
        task1 = task_generator("1", 101)
        task2 = task_generator("2", 102)
        taskDaoImpl.batch_save([task1, task2])

    def test_simple_delete(self):
        delete_query = SimpleTaskQuery()
        delete_query.status = 0
        delete_query.address = '192.168.1.2'
        taskDaoImpl.simple_delete(delete_query)

    def test_simple_query(self):
        query = SimpleTaskQuery()
        query.status = 0
        result = taskDaoImpl.simple_query(query)
        print(result)

    def test_simple_query_plus(self):
        query = SimpleTaskQuery()
        query.status = 0
        query.queryContent = "task_id, result, address"
        result = taskDaoImpl.simple_query_plus(query)
        print(result)

    def test_simple_update(self):
        update_entity = TaskDO()
        update_entity.result = "RESULT"

        query = SimpleTaskQuery()
        query.status = 0

        taskDaoImpl.simple_update(query, update_entity)

    def test_update_status(self):
        taskDaoImpl.update_status(100, '0', 1, 123456, "TEST_SUCCEED")


