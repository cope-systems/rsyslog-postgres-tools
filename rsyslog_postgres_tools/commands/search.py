from argparse import ArgumentParser
import logging
from dateutil.parser import parse

from rsyslog_postgres_tools.common.queries import search_system_events
from rsyslog_postgres_tools.common.models import DEFAULT_SYSTEM_EVENT_TEMPLATE_STR
from rsyslog_postgres_tools.common.eventlet_pg import regular_connect


def attach_search_command(subparser: ArgumentParser):
    def func(args):
        connection = regular_connect(args.postgres_connection_url)
        logging.info("Search Results:")
        for event in reversed(search_system_events(
            connection,
            opt_facility=args.facility,
            opt_priority=args.priority,
            opt_from_host=args.from_host,
            opt_event_source=args.event_source,
            opt_syslog_tag_search=args.syslog_tag,
            opt_message_search=args.message,
            opt_start_received_at=args.start_received_at,
            opt_end_received_at=args.end_received_at,
            opt_start_device_reported_time=args.start_device_reported_time,
            opt_end_device_reported_time=args.end_device_reported_time,
            limit=args.limit,
            offset=args.offset
        )):
            print(event.format(args.format_str))

    subparser.add_argument(
        "-f", "--format-str", type=str,
        help="The format string for formatting syslog events.",
        default=DEFAULT_SYSTEM_EVENT_TEMPLATE_STR
    )
    subparser.add_argument(
        "-F", "--facility", nargs="+", type=int, default=None,
        help="Facility values to search."
    )
    subparser.add_argument(
        "-P", "--priority", nargs="+", type=int, default=None,
        help="Priority values to search."
    )
    subparser.add_argument(
        "-H", "--from-host", nargs="+", type=str, default=None,
        help="Hosts to search for log messages from."
    )
    subparser.add_argument(
        "-Es", "--event-source", nargs="+", type=str, default=None,
        help="Event sources to select log messages from."
    )
    subparser.add_argument(
        "-ST", "--syslog-tag", type=str, default=None,
        help="The pattern to search on syslog tags. Uses PostgreSQL SIMILAR TO syntax."
    )
    subparser.add_argument(
        "-M", "--message", type=str, default=None,
        help="The pattern to search on messages. Uses PostgreSQL SIMILAR TO syntax."
    )
    subparser.add_argument(
        "-Sra", "--start-received-at", type=parse, default=None,
        help="The minimum ReceivedAt time to search for messages from."
    )
    subparser.add_argument(
        "-Era", "--end-received-at", type=parse, default=None,
        help="The maximum ReceivedAT time to search for messages from."
    )
    subparser.add_argument(
        "-Sdrt", "--start-device-reported-time", type=parse, default=None,
        help="The minimum device reported time to search for messages from."
    )
    subparser.add_argument(
        "-Edrt", "--end-device-reported-time", type=parse, default=None,
        help="The maximum device reported time to search for messages from."
    )
    subparser.add_argument(
        "-L", "--limit", type=int, default=100,
        help="The limit on syslog messages returned. Default: 100"
    )
    subparser.add_argument(
        "-O", "--offset", type=int, default=None,
        help="The database offset on syslog messages returned."
    )
    subparser.set_defaults(func=func)
