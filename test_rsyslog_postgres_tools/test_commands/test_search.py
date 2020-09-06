import random
import string

from unittest.mock import patch
from rsyslog_postgres_tools.main import main
from rsyslog_postgres_tools.common.queries import insert_system_event, search_system_events

rng = random.Random()
rng.seed()


def _random_string(length):
    return "".join(rng.choice(string.ascii_letters + string.digits) for _ in range(length))


class FakeStdout(object):
    def __init__(self):
        self.msgs = []

    def write(self, msg):
        self.msgs.append(msg)


def test_search_command_no_opts(initialized_db_connection, database_url,
                                main_argument_parser, fake_system_event_record):

    with initialized_db_connection:
        new_record = fake_system_event_record.copy(
            message=_random_string(32),
            from_host=_random_string(8)
        )
        new_record.id = insert_system_event(initialized_db_connection, new_record)

    assert search_system_events(initialized_db_connection)

    fake_stdout = FakeStdout()

    with patch("sys.stdout.write", fake_stdout.write):
        args = main_argument_parser.parse_args([database_url, "search"])
        main(args)

    assert any(new_record.message in line for line in fake_stdout.msgs)
    assert any(new_record.from_host in line for line in fake_stdout.msgs)


def test_search_command_no_matching_opts(initialized_db_connection, database_url,
                                         main_argument_parser, fake_system_event_record):

    with initialized_db_connection:
        new_record = fake_system_event_record.copy(
            message=_random_string(32),
            from_host=_random_string(8)
        )
        new_record.id = insert_system_event(initialized_db_connection, new_record)

    assert search_system_events(initialized_db_connection)

    fake_stdout = FakeStdout()

    with patch("sys.stdout.write", fake_stdout.write):
        args = main_argument_parser.parse_args([database_url, "search", "-H", "nonesuch"])
        main(args)

    assert not fake_stdout.msgs
    assert not any(new_record.message in line for line in fake_stdout.msgs)
    assert not any(new_record.from_host in line for line in fake_stdout.msgs)


def test_search_command_matching_opts(initialized_db_connection, database_url,
                                         main_argument_parser, fake_system_event_record):

    with initialized_db_connection:
        new_record = fake_system_event_record.copy(
            message=_random_string(32),
            from_host=_random_string(8)
        )
        new_record.id = insert_system_event(initialized_db_connection, new_record)

    assert search_system_events(initialized_db_connection)

    fake_stdout = FakeStdout()

    with patch("sys.stdout.write", fake_stdout.write):
        args = main_argument_parser.parse_args([database_url, "search", "-H", new_record.from_host])
        main(args)

    assert fake_stdout.msgs
    assert any(new_record.message in line for line in fake_stdout.msgs)
    assert any(new_record.from_host in line for line in fake_stdout.msgs)
