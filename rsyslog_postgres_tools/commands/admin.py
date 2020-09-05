from argparse import ArgumentParser


def attach_admin_command(subparser: ArgumentParser):
    def func(args):
        pass

    subparser.set_defaults(func=func)
