from argparse import ArgumentParser

from rsyslog_postgres_tools.http_server.app import run_server


def attach_run_http_server_command(subparser: ArgumentParser):
    def func(args):
        return run_server(args.postgres_connection_url, args.bind_host, args.port, suburl=args.suburl)

    subparser.add_argument("-u", "--suburl", type=str, default=None, help="The SubURL root for the application.")
    subparser.add_argument("-b", "--bind-host", type=str, default="127.0.0.1", help="IP to bind to.")
    subparser.add_argument("-p", "--port", type=int, default=8080, help="Port to serve. Default: 8080")
    subparser.set_defaults(func=func)
