import json

from ipsurv.serializer.serializer import Serializer


class JsonSerializer(Serializer):
    def __init__(self, args):
        super().__init__(args)

        self.format_params = args.fixed_format_params
        self.json = args.json
        self.json_list = args.json_list
        self.exhaustive = args.exhaustive

    def output_begin(self, mode, args, rows):
        if self.json_list:
            print('[')

    def filter_value(self, v):
        return v

    def build_row(self, data):
        all_values = data.get_values()

        values = {}

        if not self.exhaustive:
            for param in self.format_params:
                values[param] = all_values[param]
        else:
            values = all_values

        return values

    def build_error(self, error):
        return {'error': error}

    def output_complete(self, mode, args, rows):
        if self.json_list:
            print(']')

    def output(self, v):
        if self.json == 2:
            r = json.dumps(v, indent=2)
        else:
            r = json.dumps(v)

        append = ',' if self.json_list else ''

        print(r + append)

    def transform_key_labels(self, data, mode):
        pass

    def output_message(self, msg):
        pass

    def output_item(self, data):
        self.output(data.get_values())
