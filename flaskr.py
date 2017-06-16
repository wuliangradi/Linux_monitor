# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~
    A microblog example application written as Flask tutorial with
    Flask and sqlite3.
    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import sys
sys.path.append('/home/users/wuliang09/project/monitor/')
import os
from sqlite3 import dbapi2 as sqlite3
from monitor_item_check import data_check
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

reload(sys)
sys.setdefaultencoding('utf-8')
# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    EMAIL='ta@baidu.com',
    PASSWORD='flyfly'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# @app.route('/')
# def show_entries():
#     db = get_db()
#     cur = db.execute('SELECT title, text FROM entries ORDER BY id DESC')
#     entries = cur.fetchall()
#     return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['email'] != app.config['EMAIL']:
            error = 'Invalid email'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.route('/')
def home():
    links = [{"name": "login", "url": "login"},
             {"name": "show", "url": "show_entries"},
             ]
    return render_template("home.html")


@app.route('/data_monitor', methods=['GET', 'POST'])
def data_monitor():
    print request.method, request.form.get('query', None)
    if request.method == 'GET':
        result = {}
        return render_template("home.html", result=result)
    if request.method == 'POST' and request.form.get('query', None) == u"监控查询":
        baseid = request.form['baseid']
        temid = request.form['temid']
        re = data_check(baseid, temid, "拥抱的似水年华")
        result = {"baseid": re[0], "temid": re[1], "description":re[2], "table_name":re[3], "user":re[4], "state":re[5]}
        return render_template('home.html', result_query=result)
    if request.method == 'POST' and request.form.get('query', None) == u"监控测试":
        stock_no = request.form['baseid']
        print stock_no
        result = {"baseid": "baidu"}
        print request.form.getlist('user')
        return render_template('home.html', result_insert=result)
    else:
        print ">>>>"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
