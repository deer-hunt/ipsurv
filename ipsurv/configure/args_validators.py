from ipsurv.util.args_util import ArgValidator

from functools import partial

import re
import logging


class FormatValidator(ArgValidator):
    def __init__(self, profiles, params, debug=False):
        super().__init__(debug)

        self.name = 'format'
        self.profiles = profiles
        self.params = params

    def _validate(self, args):
        format = args.format

        if not format:
            raise self.arg_error('Empty value.')

        ft = format.lower()

        ft = ft if ft else 'default'

        if ft in self.profiles:
            format, params = self._create_by_profile(args, ft)
        else:
            format, params = self._parse_format(args, format)

            if len(params) == 0:
                raise self.arg_error('Format error.(' + args.format + ')')

        self._test_format(format, params)

        format, params = self._append_head(args, format, params)

        logging.log(logging.INFO, 'Fixed format:' + format)

        return format, params

    def _append_head(self, args, format, params):
        delimiter = args.fixed_delimiter

        if args.ident:
            format = '{identifier}' + delimiter + format
            params = ['identifier'] + params

        if args.add_ip:
            format = '{ip}' + delimiter + format
            params = ['ip'] + params

        if not args.no_original:
            format = '{original}' + delimiter + format
            params = ['original'] + params

        if args.sequence:
            format = '{sequence}' + delimiter + format
            params = ['sequence'] + params

        return format, params

    def _create_by_profile(self, args, profile):
        params = self.profiles[profile]

        if args.icmp:
            params.append('icmp')

        if args.tcp:
            params.append('tcp')

        if args.udp:
            params.append('udp')

        if args.http and profile != 'http':
            params.append('http')

        format = self._create_by_params(params, args)

        return format, params

    def _create_by_params(self, params, args):
        delimiter = args.fixed_delimiter

        params = self._filter_available_params(params, args)

        format = delimiter.join('{' + v + '}' for v in params)

        return format

    def _filter_available_params(self, params, args):
        def fn(v):
            if not args.group and v in ['group', 'group_int', 'group_found', 'group_status']:
                return False

            if not args.range and v == 'in_range':
                return False

            return True

        return list(filter(fn, params))

    def _parse_format(self, args, format):
        params = []

        format = re.sub(r'(\{([^{}]+?)\}|<([^<>]+?)>)', partial(self._parse_profile_param, defines=self.params, args=args, params=params), format)

        return format, params

    def _parse_profile_param(self, match, defines, args, params):
        org = match.group(0)
        param = match.group(2)
        profile = match.group(3)

        r = None

        if param:
            param = param.lower()

            if re.search(r'^[a-z0-9][a-z0-9_.]*$', param, re.IGNORECASE):
                params.append(param)
                r = org.lower()
            else:
                raise self.arg_error('Invalid param.(' + org + ')')
        else:
            profile = profile.lower()

            if profile in self.profiles:
                keys = self.profiles[profile]
                params.extend(keys)

                r = self._create_by_params(keys, args)
            else:
                raise self.arg_error('Unknown profile.(' + org + ')')

        return r

    def _test_format(self, format, params):
        data = {v: '' for v in params}

        class Dummy:
            def __getattr__(self, name):
                return None

        for k in params:
            m = re.search(r'^([^.]+)\.', k)

            if m:
                data[m.group(1)] = Dummy()

        try:
            format.format(**data)
        except Exception as e:
            raise self.arg_error('Format error.(' + str(e) + ')')


class TimeoutValidator(ArgValidator):
    def __init__(self, default=8.0, debug=False):
        super().__init__(debug)

        self.name = 'timeout'
        self.default = default

    def _validate(self, args):
        v = args.timeout

        tms = [self.default, self.default, self.default]

        if v is None:
            pass
        elif re.search(r'^[\d.]+$', v):
            t = self._parse_float(v)
            tms = [t for _ in tms]
        else:
            values = re.split(r'[,;:]', v)
            values = [self._parse_float(v) for v in values]

            for i in range(len(tms)):
                if i < len(values):
                    tms[i] = values[i]

        timeout = {'dns': tms[0], 'http': tms[1], 'reactivity': tms[2]}

        logging.log(logging.INFO, 'Fixed timeout:' + str(timeout))

        return timeout

    def _parse_float(self, v):
        v = v.strip()

        if not v:
            return self.default

        return float(v)
