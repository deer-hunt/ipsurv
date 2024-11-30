import argparse
import json
import logging
import re
from collections import Counter

from ipsurv.configure.args_validators import FormatValidator, TimeoutValidator
from ipsurv.configs import Constant
from ipsurv.core.pipeline import Pipeline
from ipsurv.util.args_util import ArgsHelper, StdinLoader
from ipsurv.util.sys_util import System


class ArgsBuilder:
    def __init__(self, config, pipeline):
        self.config = config
        self.pipeline = pipeline  # type: Pipeline

    def parse(self):
        parent_parser, args = self.init_args(self.config.PRE_ARGUMENTS)

        if not args.disable_env:
            env_ags = StdinLoader.load_env(Constant.ENV_ARGS_VAR)
        else:
            env_ags = {}

        env_conf = self._load_env_conf(Constant.ENV_CONF_VAR)

        args = self.build_args(parent_parser, self.config.APP_ARGUMENTS, env_ags, env_conf)

        return args

    def _load_env_conf(self, name):
        values = StdinLoader.load_env(name)

        env_conf = {}

        for k in self.config.ENV_CONFS:
            if k in values:
                env_conf[k] = values[k]

        return env_conf

    def init_args(self, arguments):
        parser, args = ArgsHelper.init_parser(arguments)

        ArgsHelper.init_logging(args.verbose, args.log)

        if args.verbose > 0:
            System.warn('Enable verbose mode. Current:' + str(args.verbose) + ' [Level - 1:TRACE_ERROR, 2:INFO, 3:DEBUG]')

            if args.log is not None:
                System.warn('Enable log.(File:' + args.log + ')')

        return parser, args

    def build_args(self, parent_parser, arguments, env_args, env_conf):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, parents=[parent_parser], description=Constant.APP_DESCRIPTION, epilog=Constant.APP_BOTTOM_DESC)

        self.pipeline.init_configure(arguments, env_args)

        self._prepare_arguments(parser, arguments, env_args)

        args = parser.parse_args()

        if System.is_logging():
            self.logging(args, env_args, env_conf)

        self.pipeline.pre_configure(args, env_args, env_conf)

        args.conf = env_conf

        self._configure(parser, args)

        self.pipeline.post_configure(args, env_args, env_conf)

        self._notice(args)

        return args

    def _configure(self, parser, args):
        debug = True if System.get_log_level() == logging.DEBUG else False

        try:
            args.fixed_delimiter = self._fix_delimiter(args)
            args.fixed_format, args.fixed_format_params = self._fix_format(args, debug)
            args.fixed_timeout = self._fix_timeout(args, debug)
            args.fixed_enclose = self._fix_enclose(args)
            args.fixed_ranges = self._fix_ranges(args)
            args.fixed_collectors = self._fix_collectors(args)
        except Exception as e:
            logging.log(logging.DEBUG, 'Fix arguments error.', exc_info=True)

            parser.error(e)

    def _prepare_arguments(self, parser, arguments, env_args):
        parser.add_argument('target', type=str, default=None, nargs='*', help='IP addresses or FQDN or URL.')

        arguments['group']['type'] = self._validate_group

        ArgsHelper.add_arguments(parser, arguments, env_args)

    def logging(self, args, env_args, env_conf):
        System.output_data('ENV(' + Constant.ENV_ARGS_VAR + ')', env_args)

        System.output_data('ENV(' + Constant.ENV_CONF_VAR + ')', env_conf)

        params = vars(args)

        System.output_data('ARGUMENTS', params)

        v = json.dumps(params, ensure_ascii=False)
        System.output_body('ARGUMENTS_JSON', v, level=logging.INFO)

    def _validate_group(self, v):
        v = v.strip()

        if v == '':
            v = None
        elif not (v == 'network' or re.search(r'^([\d]{1,3}|[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})$', v)):
            raise argparse.ArgumentTypeError("Illegal group value. Ex: network, 24, 255.255.255.0")

        return v

    def _fix_delimiter(self, args):
        v = args.delimiter

        if not v:
            matches = re.findall(r'[\t,;/|]', args.format)

            if len(matches) > 0:
                counter = Counter(matches)

                mc = counter.most_common(1)

                v, n = mc[0]
            else:
                v = Constant.DELIMITER_DEFAULT

        logging.log(logging.INFO, 'Fixed delimiter:' + v)

        return v

    def _fix_format(self, args, debug):
        format_validator = FormatValidator(self.config.FORMAT_PROFILES, self.config.FORMAT_PARAMS, debug=debug)

        return format_validator.validate(args)

    def _fix_timeout(self, args, debug):
        timeout_validator = TimeoutValidator(8.0, debug=debug)

        return timeout_validator.validate(args)

    def _fix_enclose(self, args):
        v = args.enclose

        if v == '1':
            v = '"'
        elif v == '2':
            v = "'"
        elif v == '3':
            v = '|'
        elif not v or v == '0':
            v = ''

        logging.log(logging.INFO, 'Fixed enclose:' + v)

        return v

    def _fix_ranges(self, args):
        ranges = re.split(r'[;, ]+', args.range)

        ranges = list(filter(lambda v: v.strip(), ranges))

        logging.log(logging.INFO, 'Fixed ranges:' + str(ranges))

        return ranges

    def _fix_collectors(self, args):
        v = args.collect.lower()

        collectors = re.split(r'[;, ]+', v)

        collectors = [v for v in collectors if v in self.config.COLLECTORS]

        logging.log(logging.INFO, 'Fixed collectors:' + str(collectors))

        return collectors

    def _notice(self, args):
        if args.json:
            if args.delimiter:
                System.warn('"delimiter" option is ignored in "json" mode.')

            if args.enclose:
                System.warn('"enclose" option is ignored in "json" mode.')
        else:
            if args.exhaustive:
                System.warn('You must use "exhaustive" option with "json" option.')

            if args.json_list:
                System.warn('You must use "json_list" option with "json" option.')

    def read_lines(self, args):
        if len(args.target) > 0:
            lines = args.target
        else:
            lines = StdinLoader.read_stdin(2.0)

        return lines
