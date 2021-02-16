# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      implementation for task dao
# Author:           tjq
# Created:          2021/2/14
# ------------------------------------------------------------------
import time
from typing import List

from persistence.query import SimpleTaskQuery
from persistence.task_dao import TaskDao
from persistence.task_do import TaskDO
from persistence.connection import get_connection, execute

DROP_TABLE__SQL = 'drop table if exists task_info'
CREATE_TABLE_SQL = '''
create table task_info (
            task_id varchar(255),
            instance_id bigint(20),
            sub_instance_id bigint(20),
            task_name varchar(255),
            task_content blob,
            address varchar(255),
            status int(5),
            result text,
            failed_cnt int(11),
            created_time bigint(20),
            last_modified_time bigint(20),
            last_report_time bigint(20),
            unique (instance_id, task_id)
            )
'''
INSERT_SQL = 'insert into task_info(task_id, instance_id, sub_instance_id, task_name, task_content, address, status, result, failed_cnt, created_time, last_modified_time, last_report_time) values (?,?,?,?,?,?,?,?,?,?,?,?)'


def prepare_insert_params(task: TaskDO):
    return task.taskId, task.instanceId, task.subInstanceId, task.taskName, task.taskContent, task.address, task.status, task.result, task.failedCnt, task.createdTime, task.lastModifiedTime, task.lastReportTime


def convert(row) -> TaskDO:
    task = TaskDO()
    task.taskId = row[0]
    task.instanceId = row[1]
    task.subInstanceId = row[2]
    task.taskName = row[3]
    task.taskContent = row[4]
    task.address = row[5]
    task.status = row[6]
    task.result = row[7]
    task.failedCnt = row[8]
    task.createdTime = row[9]
    task.lastModifiedTime = row[10]
    task.lastReportTime = row[11]
    return task


class TaskDaoImpl(TaskDao):

    def init_table(self):
        execute(DROP_TABLE__SQL)
        execute(CREATE_TABLE_SQL)

    def save(self, task: TaskDO):
        params = prepare_insert_params(task)
        execute(INSERT_SQL, params)

    def batch_save(self, tasks: List[TaskDO]):
        params_list = [prepare_insert_params(t) for t in tasks]
        conn = get_connection()
        conn.cursor().executemany(INSERT_SQL, params_list)
        conn.commit()

    def simple_delete(self, query: SimpleTaskQuery):
        sql = 'delete from task_info where ' + query.get_query_condition()
        execute(sql)

    def simple_query(self, query: SimpleTaskQuery) -> List[TaskDO]:
        sql = 'select * from task_info where ' + query.get_query_condition()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        return [convert(row) for row in rows]

    def simple_query_plus(self, query: SimpleTaskQuery) -> List[dict]:
        sql = 'select ' + query.get_query_content() + ' from task_info where ' + query.get_query_condition()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        desc = cursor.description
        return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

    def simple_update(self, query: SimpleTaskQuery, entity: TaskDO):
        sql = 'update task_info set ' + entity.gen_update_sql() + ' where ' + query.get_query_condition()
        execute(sql)

    def update_status(self, instance_id: int, task_id: str, status: int, last_report_time: int, result: str):
        now_ts = int(round(time.time() * 1000))

        sql = '''
        update task_info 
        set status = ?, last_report_time = ?, result = ?, last_modified_time = ?
        where instance_id = ? and task_id = ? 
                    '''
        update_params = (status, last_report_time, result, now_ts, instance_id, task_id)
        execute(sql, update_params)
