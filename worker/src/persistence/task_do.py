# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      'task' table
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
import time


class TaskDO(object):
    __slots__ = (
        'taskId',
        'instanceId',
        'subInstanceId',
        'taskName',
        'taskContent',
        'address',
        'status',
        'result',
        'failedCnt',
        'createdTime',
        'lastModifiedTime',
        'lastReportTime'
    )

    def __init__(self):
        self.taskId = None
        self.instanceId = None
        self.subInstanceId = None
        self.taskName = None
        self.taskContent = None
        self.address = None
        self.status = None
        self.result = None
        self.failedCnt = None
        self.createdTime = None
        self.lastModifiedTime = None
        self.lastReportTime = None

    def gen_update_sql(self) -> str:
        sql = ''
        if self.address is not None:
            sql = sql + " address = '" + self.address + "',"
        if self.status is not None:
            sql = sql + " status = " + str(self.status) + ","
        if self.result is not None:
            sql = sql + " result = '" + self.result + "',"
        if self.failedCnt is not None:
            sql = sql + " failed_cnt = " + str(self.failedCnt) + ","
        if self.lastReportTime is not None:
            sql = sql + " last_report_time = " + str(self.lastReportTime) + ","

        modify_time = self.lastModifiedTime if self.lastModifiedTime is not None else int(round(time.time() * 1000))
        return sql + " last_modified_time = " + str(modify_time)