import datetime

from rsyslog_postgres_tools.main import main
from rsyslog_postgres_tools.common.queries import insert_system_event, search_system_events


def test_clean_command(initialized_db_connection, database_url,
                       main_argument_parser, fake_system_event_record):

    with initialized_db_connection:
        new_record = fake_system_event_record.copy(
            received_at=fake_system_event_record.received_at - datetime.timedelta(days=30)
        )
        new_record.id = insert_system_event(initialized_db_connection, new_record)

    assert search_system_events(initialized_db_connection)

    args = main_argument_parser.parse_args([database_url, "clean", "-pi", "1 day"])
    main(args)

    assert not search_system_events(initialized_db_connection)

