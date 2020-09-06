import pytest

from rsyslog_postgres_tools.main import main


@pytest.mark.parametrize("apply_migrations", [False])
def test_bootstrap_command(initialized_db_connection, database_url, main_argument_parser):
    with initialized_db_connection.cursor() as c:
        c.execute("""
        select count(*) as t_count
        from information_schema.tables
        where table_schema = 'public';
        """)
        table_count = c.fetchone()["t_count"]
    assert table_count == 0

    args = main_argument_parser.parse_args([database_url, "bootstrap"])
    main(args)

    with initialized_db_connection.cursor() as c:
        c.execute("""
        select count(*) as t_count
        from information_schema.tables
        where table_schema = 'public';
        """)
        table_count = c.fetchone()["t_count"]
    assert table_count > 0
