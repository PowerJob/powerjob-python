# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      task dao interface
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
from abc import ABCMeta, abstractmethod
from typing import List
from persistence.task_do import TaskDO
from persistence.query import SimpleTaskQuery


class TaskDao(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def init_table(self):
        pass

    @abstractmethod
    def save(self, task: TaskDO):
        pass

    @abstractmethod
    def batch_save(self, *task: TaskDO):
        pass

    @abstractmethod
    def simple_delete(self, query: SimpleTaskQuery):
        pass

    @abstractmethod
    def simple_query(self, query: SimpleTaskQuery) -> List[TaskDO]:
        pass

    @abstractmethod
    def simple_query_plus(self, query: SimpleTaskQuery) -> List[dict]:
        pass

    @abstractmethod
    def simple_update(self, query: SimpleTaskQuery, entity: TaskDO):
        pass

    @abstractmethod
    def update_status(self, instance_id: int, task_id: str, status: int, last_report_time: int, result: str):
        pass