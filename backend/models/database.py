from config import *
from multiprocessing import Lock

import psycopg2
from psycopg2 import sql
import mongoengine
import numpy as np


connection = psycopg2.connect(
    host = HOST,
    port = 5432,
    user = USER,
    password = PASSWORD,
    database= DBNAME
    )

cursor_lock = Lock()

def verify_input(input):
    for value in input:
        if not clean(value):
            return False
    return True

def clean(sql):
    allow_query = True

    bad_word_list = ["drop", "table",";","--","select","delete"]
    if type(sql) is str:
        allow_query = not any(ele for ele in bad_word_list if ele in sql.lower())
        if not allow_query:
            print("SQL INJECTION ATTEMPT")
            print(sql)
    return allow_query

def check_execute(sql):
    allow_query = True

    bad_word_list = ["drop",";","--"]
    if type(sql) is str:
        allow_query = not any(ele for ele in bad_word_list if ele in sql.lower())
        if not allow_query:
            print("SQL INJECTION ATTEMPT")
            print(sql)
    return allow_query


def guid():
    return bytes([65+np.random.randint(26) for x in range(24)]).decode()

def query(sql):
    with cursor_lock:
        try:
            cursor = connection.cursor()
            ret = cursor.execute(sql)
            query_results = cursor.fetchall()
            return query_results
        except (psycopg2.errors.InFailedSqlTransaction, psycopg2.errors.InvalidRowCountInResultOffsetClause):
            print("SQL Error")
            cursor.execute("ROLLBACK")
            connection.commit()
            return None

def execute(sql):
    if check_execute(sql):
        with cursor_lock:
            cursor = connection.cursor()
            ret = cursor.execute(sql)
            connection.commit()

def execute_param(sql, params=None):
    with cursor_lock:
        cursor = connection.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        connection.commit()

def safe_format(val):
    if val is None:
        return 'NULL'
    elif type(val) is list:
        val = [sql.Identifier(str(x)).as_string(connection) for x in val]
        return f"'{{{','.join(val)}}}'"
    else:
        return sql.Identifier(str(val)).as_string(connection)


def format(val):
    if val is None:
        return 'NULL'
    elif type(val) is list or type(val) is mongoengine.base.datastructures.BaseList:
        val = [f"{str(x)}" for x in val]
        return f"'{{{','.join(val)}}}'"
    else:
        if type(val) is str:
            val = val.replace("'","''")
        return f"'{val}'"

def format_int(val):
    if val is None:
        return -1
    else:
        return f"{val}"
