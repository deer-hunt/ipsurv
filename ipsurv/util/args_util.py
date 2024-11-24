import argparse
import json
import logging
import os
import sys
from abc import ABC, abstractmethod
import select


class StrAction(argparse.Action):
    def __call__(self, parser, namespace, v, option_string=None):
        setattr(namespace, self.dest, v.replace('\\t', '\t'))


class ArgValidator(ABC):
    def __init__(self, debug=False):
        self.name = None

        self.debug = debug
        self.error = 'Argument value error.'

    def validate(self, args):
        try:
            r = self._validate(args)
        except Exception as e:
            if isinstance(e, argparse.ArgumentError) or self.debug:
                raise e
            else:
                raise self.arg_error(self.error)

        return r

    @abstractmethod
    def _validate(self, args):  # pragma: no cover
        return None

    def arg_error(self, msg):
        e = argparse.ArgumentError(None, msg)

        e.argument_name = '--' + self.name

        return e


class ArgsHelper:
    @staticmethod
    def init_parser(arguments, formatter_class=argparse.ArgumentDefaultsHelpFormatter):
        parser = argparse.ArgumentParser(add_help=False, formatter_class=formatter_class)

        ArgsHelper.add_arguments(parser, arguments, [])

        args, unknown = parser.parse_known_args()

        return parser, args

    @staticmethod
    def init_logging(verbose, log):
        if verbose > 0:
            if verbose == 1:
                level = logging.ERROR
            elif verbose == 2:
                level = logging.INFO
            else:
                level = logging.DEBUG
        else:
            level = logging.CRITICAL

        logging.basicConfig(
            filename=log,
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    @staticmethod
    def add_arguments(parser, arguments, overrides):
        for arg, options in arguments.items():
            if arg in overrides:
                options['default'] = overrides[arg]

            if options.get('action') == 'StrAction':
                options['action'] = StrAction

            parser.add_argument('--{}'.format(arg), **options)


class StdinLoader:
    @staticmethod
    def read_stdin(timeout=2.0):
        r, _, _ = select.select([sys.stdin], [], [], timeout)

        if r:
            input_data = sys.stdin.read()
            lines = input_data.splitlines()
        else:
            lines = []

        return lines

    @staticmethod
    def load_env(name):
        error = False

        env = {}

        v = os.getenv(name)

        if v is not None and v != '':
            try:
                tv = json.loads(v)

                if type(env) is dict:
                    env = tv
                else:
                    error = True

            except Exception:
                logging.log(logging.DEBUG, 'Env parse error.(' + name + ')', exc_info=True)
                error = True

        if error:
            logging.log(logging.INFO, 'Fail to load env.(' + name + ')')

        return env
