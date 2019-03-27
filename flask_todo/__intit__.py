from flask import Flask, request, make_response, render_template
import datetime


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',

    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)


    @app.route('/', methods=['GET', 'POST', 'PUT'])
    def index():
        homework = {'name': 'homework', 'complete': False, 'date_set': '3/25/19'}
        room = {'name': 'room', 'complete': False, 'date_set': '3/25/19'}
        groceries = {'name': 'groceries', 'complete': False, 'date_set': '3/25/19'}
        items = [homework, room, groceries]
        return render_template('index.html', items=items)


    @app.route("/create", methods=['GET', 'POST'])
    # This page is for creating new todos
    def create_todo():
        return render_template('create_todo.html')

    @app.route("/update", methods=['GET', 'PUT'])
    # This page is for update new todos
    def update_todo():
        return render_template('update_todo.html')

    return app
