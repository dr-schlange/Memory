import random
import time
from mydevice import *
from nallely import VirtualDevice, VirtualParameter, on

class DriftGenerator(VirtualDevice):
    """Drift Generator

    Produces a slow, organic drifting signal.
    The output wanders over time with a soft attraction
    toward a center value.

    inputs:
    * speed_cv [0.0, 5.0] init=1.0: drift speed
    * amount_cv [0.0, 1.0] init=0.1: drift amplitude
    * center_cv [-1.0, 1.0] init=0.0: attraction center
    * reset_cv [0, 1] round <rising>: reset drift state

    outputs:
    * output_cv [-1.0, 1.0]: drifting value

    type: hybrid
    category: modulation
    """
    speed_cv = VirtualParameter(name='speed', range=(0.0, 5.0), default=1.0)
    amount_cv = VirtualParameter(name='amount', range=(0.0, 1.0), default=0.1)
    center_cv = VirtualParameter(name='center', range=(-1.0, 1.0), default=0.0)
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')

    @property
    def min_range(self):
        return -1.0

    @property
    def max_range(self):
        return 1.0

    def __post_init__(self, **kwargs):
        self.value = self.center
        self.last_time = time.time()

    @on(reset_cv, edge='rising')
    def on_reset_rising(self, value, ctx):
        self.value = self.center
        self.last_time = time.time()

    def main(self, ctx):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        step = random.uniform(-1.0, 1.0)
        drift = step * self.amount * self.speed * dt
        attraction = (self.center - self.value) * 0.2 * dt
        self.value += drift + attraction
        lower, upper = self.range
        self.value = max(lower, min(upper, self.value))
        return self.value