from flask import Flask
from flask_bootstrap import Bootstrap
from peewee import  PostgresqlDatabase
import os


app = Flask(__name__)
app.config.from_pyfile('flask.cfg')
if app.config['ENV'] == 'development':
    app.config['CHROME_DRIVER'] = 'chromedriver78'
    app.config['DATABASE_NAME'] = 'sunarp'
    app.config['DATABASE_HOST'] = 'localhost'
    app.config['DATABASE_USER'] = 'postgres'
    app.config['DATABASE_PASSWORD'] = 'postgres'
    app.config['PROXY_LIST'] = ['127.0.0.1:80']

db = PostgresqlDatabase(
    app.config['DATABASE_NAME'],
    host=app.config['DATABASE_HOST'],
    port=app.config['DATABASE_PORT'],
    user=app.config['DATABASE_USER'],
    password=app.config['DATABASE_PASSWORD']
)
Bootstrap(app)


# This hook ensures that a connection is opened to handle any queries
# generated by the request.
@app.before_request
def _db_connect():
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    db.close()