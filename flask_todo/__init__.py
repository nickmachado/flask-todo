import psycopg2

from flask import Flask, request, make_response, render_template
from datetime import datetime



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='todo_app',
        DB_USER='flasktodo_user',

    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)


    from . import db
    db.init_app(app)


    @app.route('/', methods=['GET'])
    def index():
        con = db.get_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM items;")

        todo_results = cur.fetchall()
        cur.close()

        return render_template('index.html', items=todo_results, action="All")


    @app.route("/create", methods=['GET', 'POST'])
    # This page is for creating new todos
    def create_todo():
        if request.method == 'POST':
            new_item = request.form['task']

            con = db.get_db()
            cur = con.cursor()
            cur.execute("INSERT INTO items (name, date_added) VALUES (%s, %s)",(new_item, datetime.now()))

            con.commit()
            cur.close()

            return render_template('create_todo.html')

        elif request.method == 'GET':
            return render_template('create_todo.html')

            return render_template('create_todo.html')
    return app
