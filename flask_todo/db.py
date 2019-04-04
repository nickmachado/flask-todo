import psycopg2

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(
            f"dbname={current_app.config['DB_NAME']}" +
            f" user={current_app.config['DB_USER']} "

        )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        cur = db.cursor()
        cur.execute(f.read())
        cur.close()
        cur.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
      init_db()
      click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
