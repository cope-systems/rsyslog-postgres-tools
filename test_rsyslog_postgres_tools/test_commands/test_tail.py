import random
import string
import datetime
import signal

from unittest.mock import patch
from rsyslog_postgres_tools.main import main

rng = random.Random()
rng.seed()


class ExpectedException(Exception):
    pass


def _random_string(length):
    return "".join(rng.choice(string.ascii_letters + string.digits) for _ in range(length))


class FakeStdout(object):
    def __init__(self):
        self.msgs = []

    def write(self, msg):
        self.msgs.append(msg)


class FakeSelectLatest(object):
    def __init__(self, event_count, base_record):
        self.event_count = event_count
        self.base_record = base_record
        self.call_count = 0
        self.generated_events = []

    def __call__(self, *args, **kwargs):
        if self.event_count <= 0:
            raise ExpectedException
        else:
            self.call_count += 1
            self.event_count -= 1
            event = generate_random_record(self.base_record)
            self.generated_events.append(event)
            return [event]


def generate_random_record(old_record):
    new_record = old_record.copy(
        message=_random_string(32),
        from_host=_random_string(8),
        device_reported_time=datetime.datetime.now(),
        received_at=datetime.datetime.now()
    )
    return new_record


def test_tail_command(main_argument_parser, database_url, fake_system_event_record):

    args = main_argument_parser.parse_args([database_url, "-vv", "tail"])
    fake_stdout = FakeStdout()
    fake_select_latest = FakeSelectLatest(5, fake_system_event_record)

    def breakout(*args, **kwargs):
        signal.alarm(0)
        raise AssertionError("Took too long!")

    signal.signal(signal.SIGALRM, breakout)
    signal.alarm(15)

    try:
        with patch("sys.stdout.write", fake_stdout.write):
            with patch("rsyslog_postgres_tools.commands.tail.select_latest_events", fake_select_latest):
                with patch("rsyslog_postgres_tools.commands.tail.regular_connect", lambda *args, **kwargs: None):
                    main(args)
    except ExpectedException:
        signal.alarm(0)

    for record in fake_select_latest.generated_events:
        assert any(record.from_host in m for m in fake_stdout.msgs)

