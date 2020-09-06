from rsyslog_postgres_tools.common.queries import select_distinct_hosts_from_system_events, \
    search_system_events, insert_system_event, select_system_event_by_id, delete_old_system_events, \
    select_latest_events, delete_system_event
import datetime


def test_select_from_empty_database(initialized_db_connection):
    assert not select_distinct_hosts_from_system_events(initialized_db_connection)
    assert not search_system_events(initialized_db_connection)


def test_basic_system_event_crud(initialized_db_connection, fake_system_event_record):
    assert not select_distinct_hosts_from_system_events(initialized_db_connection)
    assert not search_system_events(initialized_db_connection)
    assert not select_latest_events(initialized_db_connection)

    with initialized_db_connection:
        fake_system_event_record.id = insert_system_event(
            initialized_db_connection, fake_system_event_record
        )

    assert "foobar" in select_distinct_hosts_from_system_events(initialized_db_connection)
    assert len(search_system_events(initialized_db_connection)) == 1
    assert select_system_event_by_id(initialized_db_connection, fake_system_event_record.id)
    assert len(select_latest_events(initialized_db_connection)) == 1

    with initialized_db_connection:
        delete_system_event(initialized_db_connection, fake_system_event_record)

    assert not select_distinct_hosts_from_system_events(initialized_db_connection)
    assert not search_system_events(initialized_db_connection)
    assert not select_system_event_by_id(initialized_db_connection, fake_system_event_record.id)
    assert not select_latest_events(initialized_db_connection)


def test_delete_old_events(initialized_db_connection, fake_system_event_record):
    assert not select_distinct_hosts_from_system_events(initialized_db_connection)
    assert not search_system_events(initialized_db_connection)

    old_record = fake_system_event_record.copy(
        received_at=fake_system_event_record.received_at - datetime.timedelta(days=30)
    )

    with initialized_db_connection:
        fake_system_event_record.id = insert_system_event(
            initialized_db_connection, fake_system_event_record
        )
        old_record.id = insert_system_event(
            initialized_db_connection, old_record
        )

    assert len(search_system_events(initialized_db_connection)) == 2
    assert select_system_event_by_id(initialized_db_connection, fake_system_event_record.id)
    assert select_system_event_by_id(initialized_db_connection, old_record.id)

    with initialized_db_connection:
        delete_old_system_events(initialized_db_connection, "21 days")

    assert len(search_system_events(initialized_db_connection)) == 1
    assert select_system_event_by_id(initialized_db_connection, fake_system_event_record.id)
    assert not select_system_event_by_id(initialized_db_connection, old_record.id)