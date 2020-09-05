from bottle import Bottle, HTTPResponse
from eventlet import wsgi
from bottle_swagger import SwaggerPlugin, default_server_error_handler
import eventlet
import yaml
import logging

from rsyslog_postgres_tools import SWAGGER_SPEC_PATH
from rsyslog_postgres_tools.common.eventlet_pg import create_green_psycopg_pool
from rsyslog_postgres_tools.http_server.api import attach_api_routes
from rsyslog_postgres_tools.http_server.views import attach_view_routes

app_logger = logging.getLogger(__name__)


def load_swagger_spec():
    with open(SWAGGER_SPEC_PATH, 'r') as f:
        return yaml.load(f, yaml.SafeLoader)


def api_exception_handler(exception):
    app_logger.warning("Unhandled API exception!", exc_info=True)
    return default_server_error_handler(exception)


def app_exception_plugin(callback):
    def wrapper(*args, **kwargs):
        try:
            return callback(*args, **kwargs)
        except HTTPResponse:
            raise
        except BaseException:
            app_logger.exception("Unhandled application exception!")
            raise
    return wrapper


def build_app(database_url):
    pool = create_green_psycopg_pool(database_url)
    app = Bottle()
    attach_api_routes(app, pool)
    attach_view_routes(app, pool)
    app.install(
        SwaggerPlugin(
            load_swagger_spec(),
            serve_swagger_ui=True,
            exception_handler=api_exception_handler
        )
    )
    app.install(app_exception_plugin)
    return app


def run_server(database_url, bind_host, port, suburl=None):
    app = build_app(database_url)
    if suburl:
        app.mount(suburl, app)
    wsgi.server(eventlet.listen((bind_host, port)), app)
