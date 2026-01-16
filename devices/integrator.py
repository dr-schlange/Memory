from nallely.experimental.maths import *
from nallely import VirtualDevice, VirtualParameter, on


class Integrator(VirtualDevice):
    """
    A pure mathematical integrator for emergent
    non-determinism in async feedback loops.

    inputs:
    * input_cv [-1.0, 1.0] init=0.0 round: Integrator input in integrator unit
    * gain_cv [0.0, 100.0] init=1.0: Integrator gain
    * reset_cv [0, 1.0] round: Reset integrator

    outputs:
    * out_cv [-1.0, 1.0]: output

    type: continuous
    category: math
    meta: disable default output
    """

    input_cv = VirtualParameter(
        name="input", range=(-1.0, 1.0), conversion_policy="round", default=0.0
    )
    gain_cv = VirtualParameter(name="gain", range=(0.0, 100.0), default=1.0)
    reset_cv = VirtualParameter(
        name="reset", range=(0.0, 1.0), conversion_policy="round"
    )
    out_cv = VirtualParameter(name="out", range=(-1.0, 1.0))

    @property
    def range(self):
        return (None, None)

    def __post_init__(self, **kwargs):
        self.value = 0.0
        self.last_time = time.time()
        return {"disable_output": True}

    def main(self, ctx: ThreadContext):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        self.value += self.input * self.gain * dt
        if self.value > 1.0:
            self.value = 1.0
        elif self.value < -1.0:
            self.value = -1.0
        yield (self.value, [self.out_cv])

    @on(reset_cv, edge="rising")
    def on_reset(self, value, ctx):
        self.value = 0.0
        self.last_time = time.time()
        return (0.0, [self.out_cv])
