from nallely.logicals import *
from nallely import VirtualDevice, VirtualParameter, on

class Operator(VirtualDevice):
    a_cv = VirtualParameter(name='a', range=(-128, 127))
    b_cv = VirtualParameter(name='b', range=(-128, 127))
    operator_cv = VirtualParameter(name='operator', accepted_values=('+', '-', '/', '*', 'mod', 'min', 'max', 'clamp', 'pow'))
    type_cv = VirtualParameter(name='type', accepted_values=('ondemand', 'continuous'))

    @property
    def min_range(self):
        -128

    @property
    def max_range(self):
        return 128
    operator_map = {'+': lambda a, b: a + b, '-': lambda a, b: a - b, '*': lambda a, b: a * b, '/': lambda a, b: a / b, 'mod': lambda a, b: a % b, 'min': lambda a, b: a if a < b else b, 'max': lambda a, b: a if a > b else b, 'clamp': lambda a, b: max(min(a, b), 0), 'pow': lambda a, b: a ** b}

    def store_input(self, param, value):
        if param == 'b' and self.operator == '/' and (value == 0):
            value = 0.0001
        super().store_input(param, value)

    def __init__(self, a=0, b=0, operator='+', type='ondemand', **kwargs):
        self.a = a
        self.b = b
        self.operator = operator
        self.type = type
        super().__init__(**kwargs)

    @on(operator_cv, edge='any')
    def change_operator(self, value, ctx):
        if self.type == 'ondemand':
            return self.operator_map[value](self.a, self.b)

    @on(a_cv, edge='any')
    def operation_a2b(self, value, ctx):
        if self.type == 'ondemand':
            return self.operator_map[self.operator](value, self.b)

    @on(b_cv, edge='any')
    def operation_b2a(self, value, ctx):
        if self.type == 'ondemand':
            return self.operator_map[self.operator](self.a, value)

    def main(self, ctx: ThreadContext):
        if self.type != 'continuous':
            return
        return self.operator_map[self.operator](self.a, self.b)

    @staticmethod
    def build_node(a, b, operator):
        op = Operator(operator=operator)
        op.a_cv = a.output_cv
        if isinstance(b, VirtualDevice):
            op.b_cv = b.output_cv
        else:
            op.set_parameter('b', b)
        op.start()
        return op

    def __add__(self, o):
        return self.build_node(self, o, '+')

    def __sub__(self, o):
        return self.build_node(self, o, '-')

    def __mul__(self, o):
        return self.build_node(self, o, '*')

    def __div__(self, o):
        return self.build_node(self, o, '/')