# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      monitor worker cluster status
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
import time
import threading
from typing import List


class ProcessorTrackerStatus(object):
    DISPATCH_THRESHOLD = 20
    HEARTBEAT_TIMEOUT_MS = 60000

    def __init__(self, address: str):
        self.address = address
        self.lastActiveTime = -1
        self.remainTaskNum = 0
        self.dispatched = False
        self.connected = False

    def update(self, report_time: int, remain_task: int):
        if report_time < self.lastActiveTime:
            return
        self.lastActiveTime = report_time
        self.remainTaskNum = remain_task
        self.dispatched = True
        self.connected = True

    def timeout(self) -> bool:
        if self.dispatched:
            now = int(round(time.time() * 1000))
            return now - self.lastActiveTime > ProcessorTrackerStatus.HEARTBEAT_TIMEOUT_MS
        return False

    def available(self) -> bool:
        if not self.dispatched:
            return True
        if not self.connected:
            return False
        if self.timeout():
            return False
        if self.remainTaskNum > ProcessorTrackerStatus.DISPATCH_THRESHOLD:
            return False
        return True


class ProcessorTrackerStatusHolder(object):

    def __init__(self, address_list: List[str]):

        self._lock = threading.RLock()

        self.address2Status = dict()
        for address in address_list:
            self.address2Status[address] = ProcessorTrackerStatus(address)

    def update(self, address: str, last_report_time: int, remain_task_num: int):
        try:
            self._lock.acquire()
            self.get_processor_tracker_status(address).update(last_report_time, remain_task_num)
        finally:
            self._lock.release()

    def get_processor_tracker_status(self, address: str) -> ProcessorTrackerStatus:
        res = self.address2Status[address]
        if res is None:
            try:
                self._lock.acquire()
                self.address2Status[address] = ProcessorTrackerStatus(address)
            finally:
                self._lock.release()
        return self.address2Status[address]

    def get_available_processor_tackers(self) -> List[str]:
        return [address for address in self.address2Status if self.address2Status[address].available()]

    def get_all_processor_tackers(self) -> List[str]:
        return [address for address in self.address2Status]

    def get_all_disconnected_processor_trackers(self) -> List[str]:
        return [address for address in self.address2Status if self.address2Status[address].timeout()]

    def register(self, address: str) -> bool:
        pts = self.address2Status[address]
        if pts is not None:
            return False
        self.address2Status[address] = ProcessorTrackerStatus(address)
        return True

    def remove(self, address_list: List[str]):
        for address in address_list:
            del self.address2Status[address]
