# -*- coding: utf-8 -*-

import psutil
import sqlite3
import time


def get_mem():
    mem = psutil.virtual_memory()
    mem_total = mem.total / 1024 / 1024
    mem_used = mem.used / 1024 / 1024
    mem_percent = mem_used * 1.0 / mem_total * 100
    return mem_total, mem_used, mem_percent


def create_table(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS mem
           (id INTEGER PRIMARY KEY AUTOINCREMENT, insert_time TEXT, mem_total INT, mem_used INT, mem_percent FLOAT)
        ''')
    conn.close()


def main():
    while True:
        mem_total, mem_used, mem_percent = get_mem()
        t = time.strftime('%M:%S', time.localtime())
        data = [t, mem_total, mem_used, mem_percent]
        db_name = "linux.db"
        create_table(db_name)
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('INSERT INTO mem(insert_time, mem_total, mem_used, mem_percent) VALUES (?,?,?,?)', data)
        conn.commit()
        conn.close()


if __name__ == '__main__':
    main()
