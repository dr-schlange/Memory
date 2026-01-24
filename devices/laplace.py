from nallely.experimental.maths import *
from nallely import VirtualDevice, VirtualParameter, on

class Laplace(VirtualDevice):
    """Simple Laplace transformation

    This neuron is a simple mathematical Laplace transformation applied
    following the equation:
        > out_now = (b0 * in_now) + (b1 * in_prev) - (a1 * out_prev)

    inputs:
    * input_cv [-1.0, 1.0]: transformation input
    * b0_cv [-1, 1] init=1: scaling factor for now value
    * b1_cv [-1, 1] init=1: scaling factor for previous value
    * a1_cv [-1, 1] init=0: feedback coefficient
    * gain_cv [0.001, 100] init=1: gain applied to the transformation result
    * threshold_cv [0.001, 0.999] init=0.92: gain applied to the transformation result
    * clipping_cv [soft_cubic, algebraic, clamp, tanh, linear]: type of behavior when reaching the range limit
    * reset_cv [0, 1] round <rising>: reset the transformation internal state

    outputs:
    * output_cv [-1.0, 1.0]: transformation output

    type: hybrid
    category: math
    """
    threshold_cv = VirtualParameter(name='threshold', range=(0.001, 0.999), default=0.92)
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')
    input_cv = VirtualParameter(name='input', range=(-1.0, 1.0))
    b0_cv = VirtualParameter(name='b0', range=(-1.0, 1.0), default=1.0)
    b1_cv = VirtualParameter(name='b1', range=(-1.0, 1.0), default=1.0)
    a1_cv = VirtualParameter(name='a1', range=(-1.0, 1.0), default=0.0)
    gain_cv = VirtualParameter(name='gain', range=(0.001, 100.0), default=1.0)
    clipping_cv = VirtualParameter(name='clipping', accepted_values=['soft_cubic', 'algebraic', 'clamp', 'tanh', 'linear'])

    @property
    def min_range(self):
        return -1.0

    @property
    def max_range(self):
        return 1.0

    def __post_init__(self, **kwargs):
        self.out_prev = 0
        self.in_prev = 0

    def main(self, ctx):
        in_now = self.input
        in_prev = self.in_prev
        self.out_prev = self.output if self.output is not None else 0
        out_now = self.b0 * in_now + self.b1 * in_prev - self.a1 * self.out_prev
        self.in_prev = in_now
        out_now *= self.gain
        match self.clipping:
            case 'soft_cubic':
                if out_now > 1.0:
                    out_now = 1.0
                elif out_now < -1.0:
                    out_now = -1.0
                else:
                    out_now = 1.5 * (out_now - out_now ** 3 / 3.0)
            case 'algebraic':
                out_now = out_now / math.sqrt(1.0 + out_now * out_now)
            case 'clamp':
                out_now = max(-1.0, min(1.0, out_now))
            case 'tanh':
                out_now = math.tanh(out_now)
            case 'linear':
                ...
        return out_now

    @on(reset_cv, edge='rising')
    def on_reset_rising(self, value, ctx):
        self.out_prev = 0
        self.in_prev = 0