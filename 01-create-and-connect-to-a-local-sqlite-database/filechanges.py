#!/usr/bin/env python
# or 20210324

import os
import sqlite3

def get_db_filename():
    """ Return the name of the database. """
    return os.path.splitext(os.path.basename(__file__))[0]

def connectDB(db_filename):
    """ Connect to the SQLite database. """
    db_filename = db_filename + '.db'
    try:
        conn = sqlite3.connect(db_filename)
    except BaseException as err:
        print(str(err))
        conn = None
    return conn

def queryDB(conn, query, args):
    """ Query the database. """
    result = False
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute(query, args)
        rows = cursor.fetchall()
        num_rows = len(list(rows))
        if num_rows > 0:
            result = True
    except sqlite3.OperationalError as err:
        print(str(err))
    finally:
        if cursor is not None:
            cursor.close()
    return result

def does_table_exist(table_name):
    result = False
    conn = None
    try:
        conn = connectDB(get_db_filename())
        if conn is not None:
            query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
            args=(table_name,)
            result = queryDB(conn, query, args)
    except sqlite3.OperationalError as err:
        print(str(err))
    finally:
        if conn is not None:
            conn.close()
    return result


if __name__ == '__main__':
    db_filename = get_db_filename()
    connectDB(db_filename)
    print(does_table_exist('all'))
