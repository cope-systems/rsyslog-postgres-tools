from rsyslog_postgres_tools.main import argument_parser as main_argparser
import pytest


@pytest.fixture
def main_argument_parser():
    return main_argparser