from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)
import os.path

from celery import Celery
from flask import Flask
from flask.ext.migrate import Migrate
from flask.ext.migrate import MigrateCommand
from flask.ext.appconfig import AppConfig
from flask.ext.script import Manager
from flask.ext.cors import CORS

from .database import db
from .logger import sentry

#from keen.client import KeenClient


def create_celery_app(app=None):
    app = app or create_base_app()
    celery = Celery(
        app.import_name,
        broker=app.config.get("CELERY_BROKER_URL"),
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_base_app():
    """Creates base app with sensible defaults.
    """
    app = Flask("itgetlink")
    CORS(app)
    config = AppConfig()
    default_config = "itgetlink.backend.default_config"
    config.init_app(app, default_settings=default_config)
    db.init_app(app)

    migrate_dir = os.path.join(os.path.dirname(__file__), "migrations")
    Migrate(app, db, directory=migrate_dir)

    sentry.init_app(app)
    return app


def register_blueprints(app):
    """Registers all blueprints. Basically this is temporary solution
    to avoid circular import.
    """
    from .users.views import user_api

    app.register_blueprint(user_api, url_prefix="/api/auth")


def run_cli():  # pragma: no cover
    app = create_base_app()
    register_blueprints(app)

    cli = Manager(app)
    cli.add_command("db", MigrateCommand)
    cli.run()


def create_app():  # pragma: no cover
    """Creates app with blueprints attached.
    """
    app = create_base_app()
    register_blueprints(app)
    return app
    
'''
def create_keen(app=None):
    app = app or create_base_app()
    keen = KeenClient(project_id=app.config.get("KEEN_PROJECT_ID"), write_key=app.config.get("KEEN_WRITE_KEY"), read_key=app.config.get("KEEN_READ_KEY"))
    return keen
<<<<<<< Updated upstream
'''
