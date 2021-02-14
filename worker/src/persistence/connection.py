# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# Description:      sqlite3 connection pool
# Author:           tjq
# Created:          2021/2/13
# ------------------------------------------------------------------

import os
import sqlite3
from dbutils.persistent_db import PersistentDB

path = os.path.expanduser("~/powerjob/worker.db")

POOL = PersistentDB(
    creator=sqlite3,
    database='worker.db'
)


def get_connection():
    return POOL.connection()


def execute(*args):
    conn = POOL.connection()
    conn.cursor().execute(*args)
    conn.commit()
