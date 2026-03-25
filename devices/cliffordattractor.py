from mydevice import *
from nallely import VirtualDevice, VirtualParameter, on
from nallely.codegen import gencode
import math
import time

@gencode(keep_decorator=True)
class CliffordAttractor(VirtualDevice):
    """Clifford Attractor

    Generates emergent chaotic trajectories suitable for 2D and 3D scopes.
    The motion emerges from internal feedback and nonlinear folding.

    inputs:
    * a_cv [-4.0, 4.0] init=1.7: parameter a
    * b_cv [-4.0, 4.0] init=1.3: parameter b
    * c_cv [-4.0, 4.0] init=1.0: parameter c
    * d_cv [-4.0, 4.0] init=0.7: parameter d
    * speed_cv [0.01, 5.0] init=1.0: integration speed
    * reset_cv [0, 1] round <rising>: reset state

    outputs:
    * x_cv [-2.0, 2.0]: x axis
    * y_cv [-2.0, 2.0]: y axis
    * z_cv [-2.0, 2.0]: z axis

    type: hybrid
    category: chaos
    """
    a_cv = VirtualParameter(name='a', range=(-4.0, 4.0), default=1.7)
    b_cv = VirtualParameter(name='b', range=(-4.0, 4.0), default=1.3)
    c_cv = VirtualParameter(name='c', range=(-4.0, 4.0), default=1.0)
    d_cv = VirtualParameter(name='d', range=(-4.0, 4.0), default=0.7)
    speed_cv = VirtualParameter(name='speed', range=(0.01, 5.0), default=1.0)
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')
    x_cv = VirtualParameter(name='x', range=(-2.0, 2.0))
    y_cv = VirtualParameter(name='y', range=(-2.0, 2.0))
    z_cv = VirtualParameter(name='z', range=(-2.0, 2.0))

    def __post_init__(self, **kwargs):
        self.x = 0.1
        self.y = 0.0
        self.z = 0.0
        self.last_time = time.time()

    @on(reset_cv, edge='rising')
    def on_reset(self, value, ctx):
        self.x = 0.1
        self.y = 0.0
        self.z = 0.0
        self.last_time = time.time()

    def main(self, ctx):
        now = time.time()
        dt = (now - self.last_time) * self.speed
        self.last_time = now
        nx = math.sin(self.a * self.y) + self.c * math.cos(self.a * self.x)
        ny = math.sin(self.b * self.x) + self.d * math.cos(self.b * self.y)
        nz = math.sin(self.c * self.x) + math.cos(self.d * self.y)
        self.x += (nx - self.x) * dt
        self.y += (ny - self.y) * dt
        self.z += (nz - self.z) * dt
        yield (self.x, [self.x_cv])
        yield (self.y, [self.y_cv])
        yield (self.z, [self.z_cv])

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