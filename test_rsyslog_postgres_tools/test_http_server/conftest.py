from rsyslog_postgres_tools.http_server.app import build_app
import pytest
import webtest


@pytest.fixture
def syslog_viewer_app(database_url, initialized_db_connection):
    app = build_app(database_url)
    return webtest.TestApp(app)
