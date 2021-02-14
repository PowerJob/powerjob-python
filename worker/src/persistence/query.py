# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      simple query object
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------


class SimpleTaskQuery(object):
    LINK = ' and '

    def __init__(self):
        self.taskId = None
        self.subInstanceId = None
        self.instanceId = None
        self.taskName = None
        self.address = None
        self.status = None

        # 自定义的查询条件（where 后面的语句），如 crated_time > 10086 and status = 3
        self.queryCondition = None
        # 自定义的查询条件，如 GROUP BY status
        self.otherCondition = None
        # // 查询内容，默认为 *
        self.queryContent = ' * '
        self.limit = None

    def get_query_condition(self) -> str:
        sql = ''
        if self.taskId is not None:
            sql += "task_id = '" + self.taskId + "'" + SimpleTaskQuery.LINK
        if self.subInstanceId is not None:
            sql += "sub_instance_id = " + str(self.subInstanceId) + SimpleTaskQuery.LINK
        if self.instanceId is not None:
            sql += "instance_id = " + str(self.instanceId) + SimpleTaskQuery.LINK
        if self.address is not None:
            sql += "address = '" + self.address + "'" + SimpleTaskQuery.LINK
        if self.taskName is not None:
            sql += "task_name = '" + self.taskName + "'" + SimpleTaskQuery.LINK
        if self.status is not None:
            sql += "status = " + str(self.status) + SimpleTaskQuery.LINK
        if self.queryCondition is not None:
            sql += self.queryCondition + SimpleTaskQuery.LINK

        # remove the final 'and'
        last_index = len(sql) - len(SimpleTaskQuery.LINK)
        sql = sql[0: last_index]

        if self.otherCondition is not None:
            sql += self.otherCondition

        if self.limit is not None:
            sql += " limit " + str(self.limit)

        return sql

    def get_query_content(self) -> str:
        return self.queryContent
