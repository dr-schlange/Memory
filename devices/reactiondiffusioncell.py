from mydevice import *
import time
from nallely import VirtualDevice, VirtualParameter, on
from nallely.codegen import gencode

@gencode(keep_decorator=True)
class ReactionDiffusionCell(VirtualDevice):
    """Reaction–Diffusion Cell

    A local Gray–Scott–inspired reaction–diffusion
    system suitable for visual pattern generation.

    inputs:
    * u_diffuse_cv [-1.0, 1.0] init=0.0: U diffusion input
    * v_diffuse_cv [-1.0, 1.0] init=0.0: V diffusion input
    * feed_cv [0.0, 0.1] init=0.036: feed rate (F)
    * kill_cv [0.0, 0.1] init=0.065: kill rate (k)
    * reaction_cv [0.0, 5.0] init=1.0: reaction strength
    * reset_cv [0, 1] round <rising>: reset cell chemistry

    outputs:
    * pattern_cv [-1.0, 1.0]: visual pattern (U - V)

    type: hybrid
    category: visual
    """
    u_diffuse_cv = VirtualParameter(name='u_diffuse', range=(-1.0, 1.0), default=0.0)
    v_diffuse_cv = VirtualParameter(name='v_diffuse', range=(-1.0, 1.0), default=0.0)
    feed_cv = VirtualParameter(name='feed', range=(0.0, 0.1), default=0.036)
    kill_cv = VirtualParameter(name='kill', range=(0.0, 0.1), default=0.065)
    reaction_cv = VirtualParameter(name='reaction', range=(0.0, 5.0), default=1.0)
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')
    pattern_cv = VirtualParameter(name='pattern', range=(-1.0, 1.0))

    @property
    def min_range(self):
        return -1.0

    @property
    def max_range(self):
        return 1.0

    def __post_init__(self, **kwargs):
        self.u = 1.0
        self.v = 0.0
        self.last_time = time.time()

    @on(reset_cv, edge='rising')
    def on_reset(self, value, ctx):
        self.u = 1.0
        self.v = 0.0
        self.last_time = time.time()

    def main(self, ctx):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        dt = min(dt, 0.1)
        reaction = self.u * self.v * self.v * self.reaction
        du = -reaction + self.feed * (1.0 - self.u)
        dv = reaction - (self.feed + self.kill) * self.v
        du += 0.2 * self.u_diffuse
        dv += 0.2 * self.v_diffuse
        self.u += du * dt
        self.v += dv * dt
        self.u = max(0.0, min(1.0, self.u))
        self.v = max(0.0, min(1.0, self.v))
        pattern = self.u - self.v
        yield (max(-1.0, min(1.0, pattern)), [self.pattern_cv])
        return max(-1.0, min(1.0, pattern))