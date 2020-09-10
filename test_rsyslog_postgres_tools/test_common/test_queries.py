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


def test_search_parameters(initialized_db_connection, fake_system_event_record):
    assert not select_distinct_hosts_from_system_events(initialized_db_connection)
    assert not search_system_events(initialized_db_connection)
    assert not select_latest_events(initialized_db_connection)

    records = [
        fake_system_event_record,
        fake_system_event_record.copy(
            from_host="other-host",
            message="other-host test",
            device_reported_time=datetime.datetime.now() - datetime.timedelta(days=5)
        ),
        fake_system_event_record.copy(
            from_host="router",
            message="router test",
            received_at=datetime.datetime.now() - datetime.timedelta(days=5)
        )
    ]

    with initialized_db_connection:
        for record in records:
            record.id = insert_system_event(
                initialized_db_connection, record
            )

    assert len(search_system_events(initialized_db_connection)) == len(records)
    assert len(
        search_system_events(
            initialized_db_connection,
            opt_start_received_at=datetime.datetime.now() - datetime.timedelta(days=6),
            opt_end_received_at=datetime.datetime.now() - datetime.timedelta(days=4)
        )
    ) == 1
    assert len(
        search_system_events(
            initialized_db_connection,
            opt_start_device_reported_time=datetime.datetime.now() - datetime.timedelta(days=6),
            opt_end_device_reported_time=datetime.datetime.now() - datetime.timedelta(days=4)
        )
    ) == 1
    assert len(
        search_system_events(
            initialized_db_connection,
            opt_from_host=["router", "other-host"]
        )
    ) == 2
    assert len(
        search_system_events(
            initialized_db_connection,
            opt_message_search="%other-host%"
        )
    ) == 1


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