from rsyslog_postgres_tools.common.queries import migrate_database_up
from rsyslog_postgres_tools.common.models import SystemEventRecord
from rsyslog_postgres_tools.common.eventlet_pg import regular_connect
from test_rsyslog_postgres_tools.utils import cleanup_database

import pytest
import os
import datetime


@pytest.fixture
def database_url():
    if "TEST_DATABASE_URL" not in os.environ:
        assert False, "TEST_DATABASE_URL environment variable must be set to a PostgreSQL database to run tests."
    else:
        return os.environ["TEST_DATABASE_URL"]


@pytest.fixture
def database_connection(database_url):
    connection = regular_connect(database_url)
    cleanup_database(connection)
    return connection


@pytest.fixture
def initialized_db_connection(database_url):
    connection = regular_connect(database_url)
    cleanup_database(connection)
    connection.close()
    migrate_database_up(database_url)
    return regular_connect(database_url)


@pytest.fixture
def fake_system_event_record(id=None, customer_id=1, received_at=None, device_reported_time=None,
                             facility=1, priority=1, from_host="foobar", message="foobar",
                             nt_severity=1, importance=1, event_source="foobar", event_user="foobar",
                             event_category=1, event_id=1, event_binary_data=None, max_available=1,
                             curr_usage=1, min_usage=1, max_usage=1, info_unit_id=1, sys_log_tag="foobar",
                             event_log_tag="foobar", generic_filename="foobar"):
    return SystemEventRecord(
        id,
        customer_id,
        received_at or datetime.datetime.utcnow(),
        device_reported_time or datetime.datetime.utcnow(),
        facility,
        priority,
        from_host,
        message,
        nt_severity,
        importance,
        event_source,
        event_user,
        event_category,
        event_id,
        event_binary_data,
        max_available,
        curr_usage,
        min_usage,
        max_usage,
        info_unit_id,
        sys_log_tag,
        event_log_tag,
        generic_filename
    )