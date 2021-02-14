# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      system health info
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
import os
import multiprocessing


class SystemMetrics(object):

    def __init__(self):
        # cpu
        self.cpuProcessors = multiprocessing.cpu_count()
        self.cpuLoad = None

        # memory
        self.jvmUsedMemory = None
        self.jvmMaxMemory = None
        self.jvmMemoryUsage = None

        # disk
        disk_info = os.statvfs('/')
        total_size = disk_info.f_blocks * disk_info.f_bsize / 1024 / 1024 / 1024
        free_size = disk_info.f_bsize * disk_info.f_bavail / 1024 / 1024 / 1024
        self.diskUsed = total_size - free_size
        self.diskTotal = total_size
        self.diskUsage = round(free_size / total_size * 100, 2)

        # need to calculate by worker
        self.score = 1
