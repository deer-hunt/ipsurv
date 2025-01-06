import io
import re
import tokenize

'''
ev_parser = EvaluationParser({
    'a': {'type': int},
    'b': {'type': int, 'single': True},
    'c': {'type': int},
    'd': {'type': lambda v: v.upper()},
    'e': {'type': float},
    'f': {'type': lambda v: v.upper(), 'types': method, 'list': True, 'single': True},
})

value = 'a>= 1; a<6 ; b=8; c=80,443; d=a,b; e=4.5'

ev_parser.parse(value)
'''


class EvaluationParser:
    OPERATOR_EQUAL = 1
    OPERATOR_NOT_EQUAL = 2
    OPERATOR_GREATER = 4
    OPERATOR_LESS = 8

    def __init__(self, rules=None):
        self.rules = rules
        self.items = {}

    def initialize(self, rules):
        self.rules = rules

    def parse(self, rule_value):
        if self.rules is None:
            raise Exception('Rules don\'t exist.')

        self.items = {}

        readline = io.StringIO(rule_value).readline
        tokens = tokenize.generate_tokens(readline)

        cur_var = None
        cur_op = 0
        cur_values = []

        for tok in tokens:
            if tok.type == tokenize.NAME:
                if cur_var is None:
                    cur_var = tok.string
                else:
                    cur_values.append(tok.string)
            elif tok.type == tokenize.OP:
                if re.search(r'^[!=<>]+$', tok.string):
                    cur_op = self._add_operators(cur_op, tok.string)
                elif tok.string == ';':
                    self._append_item(cur_var, cur_op, cur_values)
                    cur_var = None
                    cur_op = 0
                    cur_values = []
                elif tok.string == '-':
                    next_token = next(tokens)

                    if next_token.type == tokenize.NUMBER:
                        cur_values.append('-' + next_token.string)
                    else:
                        self._raise_parse_error(cur_var)
            elif tok.type == tokenize.NUMBER:
                cur_values.append(tok.string)
            elif tok.type == tokenize.NEWLINE or tok.type == tokenize.ENDMARKER:
                continue

        if cur_var and cur_op:
            self._append_item(cur_var, cur_op, cur_values)
            cur_var = None
            cur_op = 0

        if cur_var or cur_op:
            self._raise_parse_error(rule_value)

        return self.items

    def _add_operators(self, cur_op, value):
        if re.search(r'!=', value):
            cur_op |= self.OPERATOR_NOT_EQUAL
        elif re.search(r'=', value):
            cur_op |= self.OPERATOR_EQUAL

        if re.search(r'>', value):
            cur_op |= self.OPERATOR_GREATER

        if re.search(r'<', value):
            cur_op |= self.OPERATOR_LESS

        return cur_op

    def _append_item(self, cur_var, cur_op, cur_values):
        if cur_var in self.rules:
            rule = self.rules[cur_var]

            try:
                self._append_item_by_rule(rule, cur_var, cur_op, cur_values)
            except Exception:
                self._raise_parse_error(cur_var)
        else:
            if cur_var is not None:
                raise EvaluationParserException("Unknown variable.({})".format(cur_var))

    def _append_item_by_rule(self, rule, cur_var, cur_op, cur_values):
        value_type = rule.get('type')

        if value_type:
            if value_type == int:
                cur_values = list(map(lambda v: int(v), cur_values))
            elif value_type == float:
                cur_values = list(map(lambda v: float(v), cur_values))
            elif callable(value_type):
                cur_values = list(map(value_type, cur_values))

        if len(cur_values) >= 2 or rule.get('list'):
            types = rule.get('types')

            if types:
                cur_values = types(cur_values)

            v = cur_values
        else:
            v = cur_values[0]

        item = {'op': cur_op, 'value': v}

        if rule.get('single'):
            self.items[cur_var] = item
        else:
            if cur_var not in self.items:
                self.items[cur_var] = []

            self.items[cur_var].append(item)

    def _raise_parse_error(self, name):
        raise EvaluationParserException("Parse error.({})".format(name))

    def evaluate(self, name, v):
        rule = self.items.get(name)

        success = False

        if rule is not None and v is not None:
            if not isinstance(rule, list):
                success = self._evaluate_value(rule, v)
            else:
                success = all(self._evaluate_value(drule, v) for drule in rule)

        return success

    def _evaluate_value(self, rule, iv):
        success = False

        dv = rule['value']
        op = rule['op']

        if not isinstance(dv, list):
            if op & self.OPERATOR_NOT_EQUAL and (dv != iv):
                return True

            if op & self.OPERATOR_EQUAL and (dv == iv):
                success = True

            if op & self.OPERATOR_GREATER and (dv < iv):
                success = True

            if op & self.OPERATOR_LESS and (dv > iv):
                success = True
        else:
            if iv in dv:
                success = True

        return success

    def get(self, name):
        return self.items.get(name)

    def get_value(self, name, index=0):
        rule = self.rules[name]

        if rule.get('single'):
            item = self.items.get(name)
        else:
            item = self.items.get(name)[index]

        return item['value']

    def get_rule(self, name):
        return self.rules[name]

    def assigned(self, name):
        return (name in self.items)

    def is_empty(self):
        return (len(self.items) == 0)

    def get_items(self):
        return self.items


class EvaluationParserException(Exception):
    pass
