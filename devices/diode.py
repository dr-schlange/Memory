from mydevice import *
from nallely import VirtualDevice, VirtualParameter, on

class Diode(VirtualDevice):
    """Diode

    A simple signal diode.
    Values below the threshold are blocked.
    Values above the threshold are passed with an optional gain.

    inputs:
    * input_cv [-1.0, 1.0] <any>: incoming signal
    * threshold_cv [-1.0, 1.0] init=0.0: diode threshold
    * gain_cv [0.0, 10.0] init=1.0: gain applied above threshold

    outputs:
    * output_cv [-1.0, 1.0]: rectified output

    type: reactive
    category: math
    """
    input_cv = VirtualParameter(name='input', range=(-1.0, 1.0))
    threshold_cv = VirtualParameter(name='threshold', range=(-1.0, 1.0), default=0.0)
    gain_cv = VirtualParameter(name='gain', range=(0.0, 10.0), default=1.0)

    @property
    def min_range(self):
        return -1.0

    @property
    def max_range(self):
        return 1.0

    @on(input_cv, edge='any')
    def on_input_any(self, value, ctx):
        if value == 0:
            return 0
        if value <= self.threshold:
            return 0
        out = (value - self.threshold) * self.gain
        lower, upper = self.range
        out = max(lower, min(upper, out))
        return out