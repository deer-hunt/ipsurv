import base64
import codecs
import re
import sys


class DataInput:
    INPUT_RAW = 'NONE'
    INPUT_TEXT = 'TEXT'
    INPUT_BINARY = 'BINARY'
    INPUT_HEX = 'HEX'
    INPUT_BASE64 = 'BASE64'

    def __init__(self, mode=None):
        self.mode = mode

    def initialize(self, mode):
        self.mode = mode

    def get_data(self, input_data):
        if self.mode == self.INPUT_TEXT:
            input_data = input_data.replace("\\n", "\n")

            input_data = input_data.encode()
        elif self.mode == self.INPUT_BINARY:
            input_data = codecs.decode(input_data, 'unicode_escape').encode('latin1')
        elif self.mode == self.INPUT_HEX:
            input_data = self.decode_hex(input_data)
        elif self.mode == self.INPUT_BASE64:
            input_data = self.decode_base64(input_data)
        elif self.mode == self.INPUT_RAW or not self.mode:
            pass
        else:
            raise Exception('Unknown input mode.')

        return input_data

    def decode_hex(self, hex_data):
        hex_data = re.sub(r'\s', '', hex_data)

        try:
            if len(hex_data) % 2 != 0:
                raise Exception()

            binary = bytes.fromhex(hex_data)
        except Exception:
            raise Exception('Hex data decode error.')

        return binary

    def decode_base64(self, base64_data):
        try:
            base64_binary = base64_data.encode('utf-8')

            binary = base64.b64decode(base64_binary)
        except Exception:
            raise Exception('Base64 data decode error.')

        return binary


class DataOutput:
    OUTPUT_TEXT = 'TEXT'
    OUTPUT_BINARY = 'BINARY'
    OUTPUT_HEX = 'HEX'
    OUTPUT_BASE64 = 'BASE64'

    def __init__(self, mode=None):
        self.mode = mode

    def initialize(self, mode):
        self.mode = mode

    def get_data(self, data):
        v = None

        if self.mode == self.OUTPUT_TEXT:
            v = data.decode('utf-8', errors='ignore')
        elif self.mode == self.OUTPUT_BINARY:
            v = data
        elif self.mode == self.OUTPUT_HEX:
            v = self.get_hex_data(data)
        elif self.mode == self.OUTPUT_BASE64:
            v = self.get_base64_data(data)
        else:
            raise Exception('Unknown output mode.')

        return v

    def get_hex_data(self, data):
        data = ''.join(f'{byte:02x} ' for byte in data)

        return data

    def get_base64_data(self, data):
        base64_data = base64.b64encode(data)

        return base64_data.decode('utf-8')

    def output_binary(self, data):
        print(self.get_data(data), flush=True)


class InteractiveInput:
    def __init__(self, multiline=False):
        self.multiline = multiline
        self.lines = ''

    def get_input(self):
        if not self.multiline:
            input = self.get_line()
        else:
            input = self.get_stdin_read()

        return input

    def get_line(self):
        line = input()

        self.lines += line + '\n'

        lines = self.lines

        if not (re.search(r'(\r\n|\r|\n){2}$', lines) and lines.strip()):
            return None

        self.lines = ''

        return lines

    def get_stdin_read(self):
        return sys.stdin.read() + '\n'
