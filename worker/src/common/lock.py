# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      Lock
# Author:           tjq
# Created:          2021/2/16
# ------------------------------------------------------------------
import threading


class SegmentLock(object):

    def __init__(self, concurrency: int):
        self._mask = concurrency - 1
        self._locks = [threading.RLock() for i in range(0, concurrency)]

    def lock(self, lock_id: int):
        self._locks[lock_id & self._mask].acquire()

    def unlock(self, lock_id: int):
        self._locks[lock_id & self._mask].release()