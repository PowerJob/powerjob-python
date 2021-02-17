# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      maintain TaskTracker and ProcessorTracker
# Author:           tjq
# Created:          2021/2/17
# ------------------------------------------------------------------
import threading
from typing import List
from core.task_tracker import TaskTracker
from core.processor_tracker import ProcessorTracker


class TaskTrackerPool(object):

    _lock = threading.RLock()
    instanceId2TaskTracker = dict()

    @staticmethod
    def get_task_tracker(instance_id) -> TaskTracker:
        return TaskTrackerPool.instanceId2TaskTracker.get(instance_id)

    @staticmethod
    def remove(instance_id) -> TaskTracker:
        return TaskTrackerPool.instanceId2TaskTracker.pop(instance_id)

    @staticmethod
    def atomic_create_task_tracker(instance_id, func):
        TaskTrackerPool._lock.acquire()
        try:
            tt = TaskTrackerPool.instanceId2TaskTracker.get(instance_id)
            if tt is None:
                TaskTrackerPool.instanceId2TaskTracker[instance_id] = func()
        finally:
            TaskTrackerPool._lock.release()


class ProcessorTrackerPool(object):

    _lock = threading.RLock()
    # instanceId -> (TaskTrackerAddress -> ProcessorTracker)
    processorTrackerPool = dict()

    @staticmethod
    def get_processor_tracker(instance_id, address, creator) -> ProcessorTracker:
        ProcessorTrackerPool._lock.acquire()
        try:
            store = ProcessorTrackerPool.processorTrackerPool.get(instance_id)
            if store is None:
                store = dict()
                ProcessorTrackerPool.processorTrackerPool[instance_id] = store
            pt = store.get(address)
            if pt is None:
                pt = creator()
                store[address] = pt
            return pt
        finally:
            ProcessorTrackerPool._lock.release()

    @staticmethod
    def remove(instance_id) -> List[ProcessorTracker]:
        ProcessorTrackerPool._lock.acquire()
        try:
            pt_dict = ProcessorTrackerPool.processorTrackerPool.pop(instance_id)
            return [pt_dict[address] for address in pt_dict]
        finally:
            ProcessorTrackerPool._lock.release()
