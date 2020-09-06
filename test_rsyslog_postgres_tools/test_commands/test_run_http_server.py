import datetime

from unittest.mock import patch
from rsyslog_postgres_tools.main import main


def test_run_http_server_command(initialized_db_connection, database_url,
                                 main_argument_parser):
    args = main_argument_parser.parse_args([database_url, "run_http_server"])
    with patch("eventlet.wsgi.server") as wsgi_server:
        with patch("eventlet.listen") as eventlet_listen:
            main(args)
            assert wsgi_server.call_count > 0
            assert eventlet_listen.call_count > 0
