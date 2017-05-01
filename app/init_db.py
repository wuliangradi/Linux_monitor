# -*- coding: utf-8 -*-

import sqlite3

db_name = "flaskr.db"


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect("flaskr.db")
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = connect_db()
    sql = '''
                create table if not EXISTS entries (
                id integer primary key autoincrement,
                title text not null,
                'text' text not null
                );
              '''
    db.cursor().execute(sql)
    db.commit()

init_db()