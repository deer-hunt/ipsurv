import logging

from ipsurv.configs import Config, Constant
from ipsurv.core.pipeline import Pipeline
from ipsurv.survey_ips import SurveyIps
from ipsurv.survey_self import SurveySelf
from ipsurv.util.sys_util import System
from ipsurv import __version__


class IpSurvCmd:
    def __init__(self, factory):
        self.factory = factory
        self.pipeline = self.factory.create_pipeline()  # type: Pipeline
        self.config = self.factory.get_config()  # type: Config

    def run(self):
        args, rows = self._parse_args()

        if args.version:
            self._output_version()

        serializer = self.factory.create_serializer(args)

        self.pipeline.initialize(self.config, serializer)

        data_factory = self.factory.create_value_data_factory(args, self.config)

        num = len(rows)
        mode = self._detect_survey_mode(num, rows)

        self.pipeline.begin_process(mode, args, rows)

        if num >= 1:
            if mode == Constant.MODE_SURVEY_IPS:
                self._survey_ips(args, data_factory, serializer, rows)
            else:
                self._survey_self(args, data_factory, serializer)
        else:
            System.warn('No target data.')

        self.pipeline.complete_process(mode, args, rows)

    def _detect_survey_mode(self, num, rows):
        if num == 1 and 'self' in rows[0].lower():
            mode = Constant.MODE_SURVEY_SELF
        else:
            mode = Constant.MODE_SURVEY_IPS

        return self.pipeline.detect_survey_mode(mode)

    def _parse_args(self):
        args_builder = self.factory.create_args_builder(self.config, self.pipeline)

        args = args_builder.parse()

        rows = args_builder.read_lines(args)

        return args, rows

    def _survey_ips(self, args, data_factory, serializer, rows):
        logging.log(logging.INFO, 'MODE:SURVEY_IPS')

        survey_ips = self._build(args, data_factory, serializer)

        survey_ips.initialize()

        survey_ips.dispatch(rows, args)

    def _build(self, args, data_factory, serializer):
        dns_resolver = self.factory.create_dns_resolver(args)

        target_parser = self.factory.create_target_parser(args, self.pipeline, dns_resolver)

        _collectors = self.factory.create_collectors(args, dns_resolver)

        collectors = [_collectors[key] for key in args.fixed_collectors]

        reactivities = self.factory.create_reactivities(args)

        return SurveyIps(args, self.config, data_factory, target_parser, collectors, reactivities, self.pipeline, serializer)

    def _survey_self(self, args, data_factory, serializer):
        logging.log(logging.INFO, 'MODE:SURVEY_SELF')

        dns_resolver = self.factory.create_dns_resolver(args)

        server_reactivity = self.factory.create_server_reactivity(args)

        collector = self.factory.create_self_collector(args, dns_resolver, server_reactivity)

        survey_self = SurveySelf(args, self.config, data_factory, collector, self.pipeline, serializer)

        survey_self.initialize()

        survey_self.dispatch()

    def _output_version(self):
        System.exit(Constant.APP_NAME + ' ' + __version__)
