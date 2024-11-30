import logging
import time

from ipsurv.configs import Constant
from ipsurv.core.pipeline import Pipeline
from ipsurv.core.target_groups import TargetGroups
from ipsurv.core.target_parser import TargetParser
from ipsurv.core.entity import HeaderTarget
from ipsurv.serializer.serializer import Serializer
from ipsurv.util.sys_util import AppException, System


class SurveyIps:
    def __init__(self, args, config, data_factory, target_parser, collectors, reactivities, pipeline, serializer):
        self.config = config
        self.data_factory = data_factory
        self.target_parser = target_parser  # type: TargetParser
        self.target_groups = TargetGroups(args, pipeline)

        self.collectors = collectors
        self.reactivities = reactivities

        self.pipeline = pipeline  # type: Pipeline
        self.serializer = serializer  # type: Serializer

    def initialize(self):
        for collector in self.collectors:
            collector.initialize()

        for reactivity in self.reactivities:
            reactivity.initialize()

    def dispatch(self, rows, args):
        if args.headers:
            self._output_headers(args)

        sequence = 0

        for row in rows:
            sequence += 1

            if (args.begin > sequence) or (args.end > 0 and args.end < sequence):
                continue

            self._survey_row(sequence, row, args)

    def _output_headers(self, args):
        headers = self.serializer.create_labels(args.fixed_format_params, args.headers)
        target = HeaderTarget()

        data = self.data_factory.build(headers)

        data.set_header(True)
        data.set('target', target)

        self.pipeline.pre_output_headers(data)

        row = self.pipeline.build(data, target)

        self.pipeline.output_result(row)

    def _survey_row(self, sequence, original, args):
        data = self.data_factory.create()

        data.set('sequence', sequence)
        data.set('original', original)

        try:
            original = self.pipeline.pre_target_parse(data, original)

            target = self.target_parser.parse(data, original, args)

            self._survey_target(data, target, args)

            row = self.pipeline.build(data, target)

            if not target.identifier_int:
                time.sleep(0.2)  # Buffer time
        except Exception as e:
            level = logging.ERROR if not isinstance(e, AppException) else logging.DEBUG

            logging.log(level, str(e), exc_info=True)

            row = self.pipeline.build_error(str(e))

        self.pipeline.output_result(row)

    def _survey_target(self, data, target, args):
        self.pipeline.pre_collect(data, target, args)

        skip = False

        if target.status == Constant.STATUS_EXIST:
            group = self.target_groups.find_group(data, target)

            requires = []

            if not group or not args.skip_duplicate:
                requires = self._survey_by_collectors(self.collectors, target, args, data, True)
            else:
                logging.info('SKIP:IP->' + target.identifier + ',GROUP->' + str(group.value))

                skip = True

            if not skip or args.skip_duplicate < 2:
                requires += self._survey_by_collectors(self.reactivities, target, args, data, False)

            success = self._finish(data, args, requires)
            data.set('success', success)

            if len(data.get('requests')) == 0:
                self.target_groups.put_group(data, target, args.group, None)

        self.pipeline.post_collect(data, target, args, skip)

        if System.is_logging():
            System.output_data('COLLECTED_DATA', data.get_values())
            System.output_data('REQUESTS', data.get('requests'), logging.DEBUG)

    def _survey_by_collectors(self, collectors, target, args, data, is_source):
        requires = []

        for collector in collectors:
            collectors = self._survey_by_collector(collector, target, args, data, is_source)

            requires += collectors

        return requires

    def _survey_by_collector(self, collector, target, args, data, is_source):
        name = collector.get_name()
        requires = collector.get_requires()

        self.pipeline.pre_request(data, name, collector)

        if self._require_request(data, requires) or len(requires) == 0 or args.all_collect:
            success, response, response_time = collector.request(target)

            self.pipeline.post_request(data, name, collector, success, response)

            if is_source:
                self._update_group(data, collector, target, args, response)

            collector.build_data(target, data, success, response, response_time)

            data.update('requests', lambda v: v + [name])
        else:
            logging.log(logging.DEBUG, 'UNNECESSARY:' + name)

        return requires

    def _require_request(self, data, keys):
        for param in data.get_data().keys():
            v = data.get(param)

            if ((v is None or v is False) and param in keys):
                return True

        return False

    def _finish(self, data, args, requires):
        success = not self._require_request(data, args.fixed_format_params)

        for k, v in data.get_data().items():
            if v is None:
                if k in requires:
                    v = ''
                elif k not in self.config.FORMAT_PARAMS:
                    v = '-'

                data.set(k, v)

        return success

    def _update_group(self, data, collector, target, args, response):
        if not data.get('group_int'):
            cidr = collector.get_cidr(response)

            group = self.target_groups.put_group(data, target, args.group, cidr)

            if group:
                logging.info('GROUP:' + str(group.value))
