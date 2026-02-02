from mydevice import *
from nallely import VirtualDevice, VirtualParameter, on
from nallely.codegen import gencode

@gencode(keep_decorator=True)
class EchoWithoutDelay(VirtualDevice):
    """Echo Without Delay Lines

    Creates echo-like persistence using recursive
    smoothing and feedback, without storing past samples.

    inputs:
    * input_cv [-1.0, 1.0] <any>: input signal
    * smear_cv [0.0, 1.0] init=0.2: temporal smearing
    * decay_cv [0.0, 1.0] init=0.5: echo strength
    * feedback_cv [0.0, 0.99] init=0.6: tail persistence
    * reset_cv [0, 1] round <rising>: clear echo state

    outputs:
    * output_cv [-1.0, 1.0]: echoed signal

    type: hybrid
    category: temporal
    """
    input_cv = VirtualParameter(name='input', range=(-1.0, 1.0))
    smear_cv = VirtualParameter(name='smear', range=(0.0, 1.0), default=0.2)
    decay_cv = VirtualParameter(name='decay', range=(0.0, 1.0), default=0.5)
    feedback_cv = VirtualParameter(name='feedback', range=(0.0, 0.99), default=0.6)
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')

    @property
    def min_range(self):
        return -1.0

    @property
    def max_range(self):
        return 1.0

    def __post_init__(self, **kwargs):
        self.shadow = 0.0
        self.input_value = 0.0

    @on(input_cv, edge='any')
    def on_input_any(self, value, ctx):
        self.input_value = value

    @on(reset_cv, edge='rising')
    def on_reset_rising(self, value, ctx):
        self.shadow = 0.0

    def main(self, ctx):
        self.shadow += (self.input_value - self.shadow) * self.smear
        self.shadow *= self.feedback
        out = self.input_value + self.shadow * self.decay
        lower, upper = self.range
        return max(lower, min(upper, out))