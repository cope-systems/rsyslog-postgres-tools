from argparse import ArgumentParser
import logging

from rsyslog_postgres_tools.common.queries import migrate_database_up

bootstrap_logger = logging.getLogger(__name__)


def attach_bootstrap_command(subparser: ArgumentParser):
    def func(args):
        bootstrap_logger.info("Applying migrations...")
        migrate_database_up(args.postgres_connection_url)
        bootstrap_logger.info("Migration completed.")

    subparser.set_defaults(func=func)
