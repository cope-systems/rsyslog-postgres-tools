from argparse import ArgumentParser
import time

from rsyslog_postgres_tools.common.queries import select_latest_events
from rsyslog_postgres_tools.common.models import DEFAULT_SYSTEM_EVENT_TEMPLATE_STR
from rsyslog_postgres_tools.common.eventlet_pg import regular_connect


def attach_tail_command(subparser: ArgumentParser):
    def func(args):
        connection = regular_connect(args.postgres_connection_url)
        last_received_at = None
        while True:
            if not last_received_at:
                last_events = select_latest_events(connection, limit=3)
            else:
                last_events = select_latest_events(connection, min_received_at=last_received_at)
            for event in reversed(last_events):
                print(event.format(args.format_str))
            if last_events:
                last_received_at = max(e.received_at for e in last_events)
            time.sleep(args.poll_interval)

    subparser.add_argument(
        "-f", "--format-str", type=str,
        help="The format string for formatting syslog events.",
        default=DEFAULT_SYSTEM_EVENT_TEMPLATE_STR
    )
    subparser.add_argument(
        "-pi", "--poll-interval", type=float,
        help="The database poll interval in seconds.",
        default=1.0
    )
    subparser.set_defaults(func=func)
