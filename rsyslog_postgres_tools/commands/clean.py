from argparse import ArgumentParser
import logging

from rsyslog_postgres_tools.common.queries import delete_old_system_events
from rsyslog_postgres_tools.common.eventlet_pg import regular_connect

clean_logger = logging.getLogger(__name__)


def attach_clean_command(subparser: ArgumentParser):
    def func(args):
        clean_logger.info("Beginning log cleaning process. Purge interval: {0}".format(args.purge_interval))
        conn = regular_connect(args.postgres_connection_url)
        try:
            clean_logger.debug("Database transaction opened..")
            with conn as transaction:
                clean_logger.debug("Transaction opened..")
                event_deleted_count = delete_old_system_events(transaction, args.purge_interval)
                clean_logger.info("{0} system events purged from database.".format(event_deleted_count))
        finally:
            clean_logger.debug("Closing database connection.")
            conn.close()
        clean_logger.info("Database old events clean-up completed successfully!")

    subparser.add_argument(
        "-pi", "--purge-interval", type=str,
        help="An interval as understood by PostgreSQL for the time interval going backwards from NOW() to"
             "purge system events based on the RecievedAt field. Default: 21 Days", default="21 Days")
    subparser.set_defaults(func=func)
