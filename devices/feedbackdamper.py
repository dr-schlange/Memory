from mydevice import *
import time
from nallely import VirtualDevice, VirtualParameter, on
from nallely.codegen import gencode

@gencode(keep_decorator=True)
class FeedbackDamper(VirtualDevice):
    """Feedback Damper

    Dynamically reduces signal gain when instability
    is detected, and slowly restores it when stable.

    inputs:
    * input_cv [-1.0, 1.0] <any>: signal to monitor
    * threshold_cv [0.0, 5.0] init=1.0: instability threshold
    * attack_cv [0.0, 10.0] init=3.0: damping speed
    * release_cv [0.0, 5.0] init=0.5: recovery speed
    * min_gain_cv [0.0, 1.0] init=0.1: minimum gain
    * reset_cv [0, 1] round <rising>: reset damper

    outputs:
    * output_cv [-1.0, 1.0]: damped signal

    type: hybrid
    category: control
    """
    input_cv = VirtualParameter(name='input', range=(-1.0, 1.0))
    threshold_cv = VirtualParameter(name='threshold', range=(0.0, 5.0), default=1.0)
    attack_cv = VirtualParameter(name='attack', range=(0.0, 10.0), default=3.0)
    release_cv = VirtualParameter(name='release', range=(0.0, 5.0), default=0.5)
    min_gain_cv = VirtualParameter(name='min_gain', range=(0.0, 1.0), default=0.1)
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')
    output_cv = VirtualParameter(name='output', range=(-1.0, 1.0))

    @property
    def min_range(self):
        return -1.0

    @property
    def max_range(self):
        return 1.0

    def __post_init__(self, **kwargs):
        self.last_value = 0.0
        self.activity = 0.0
        self.gain = 1.0
        self.last_time = time.time()

    @on(input_cv, edge='any')
    def on_input_any(self, value, ctx):
        delta = abs(value - self.last_value)
        self.last_value = value
        self.activity += delta

    @on(reset_cv, edge='rising')
    def on_reset_rising(self, value, ctx):
        self.activity = 0.0
        self.gain = 1.0
        self.last_value = 0.0
        self.last_time = time.time()

    def main(self, ctx):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        if self.activity > self.threshold:
            self.gain -= self.attack * dt
        else:
            self.gain += self.release * dt
        self.gain = max(self.min_gain, min(1.0, self.gain))
        self.activity *= max(0.0, 1.0 - 2.0 * dt)
        return self.last_value * self.gain

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...

    def main(self, ctx):
        ...