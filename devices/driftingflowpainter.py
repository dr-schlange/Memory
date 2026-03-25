from mydevice import *
from nallely import VirtualDevice, VirtualParameter, on
from nallely.codegen import gencode
import math
import time
import random

@gencode(keep_decorator=True)
class DriftingFlowPainter(VirtualDevice):
    """Drifting Flow Painter

    This neuron generates non-deterministic 2D patterns by advecting
    a moving point through a slowly drifting, self-mutating flow field.
    The system has memory, noise and feedback sensitivity, which leads
    to emergent organic shapes when visualized on a scope.

    inputs:
    * speed_cv [0.0, 5.0] init=1.0:
        particle movement speed
    * curl_cv [0.0, 5.0] init=1.0:
        rotational strength of the flow field
    * drift_cv [0.0, 2.0] init=0.2:
        slow mutation rate of the internal field
    * noise_cv [0.0, 2.0] init=0.3:
        stochastic influence (non-determinism)
    * reset_cv [0, 1] round <rising>:
        reset particle and field state

    outputs:
    * x_cv [-5.0, 5.0]:
        x coordinate for 2D scope
    * y_cv [-5.0, 5.0]:
        y coordinate for 2D scope

    type: hybrid
    category: generative
    """
    speed_cv = VirtualParameter(name='speed', range=(0.0, 5.0), default=1.0)
    curl_cv = VirtualParameter(name='curl', range=(0.0, 5.0), default=1.0)
    drift_cv = VirtualParameter(name='drift', range=(0.0, 2.0), default=0.2)
    noise_cv = VirtualParameter(name='noise', range=(0.0, 2.0), default=0.3)
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')
    x_cv = VirtualParameter(name='x', range=(-5.0, 5.0))
    y_cv = VirtualParameter(name='y', range=(-5.0, 5.0))

    def __post_init__(self, **kwargs):
        self.x = random.uniform(-1.0, 1.0)
        self.y = random.uniform(-1.0, 1.0)
        self.fx = random.uniform(0.0, 10.0)
        self.fy = random.uniform(0.0, 10.0)
        self.last_time = time.time()

    @on(reset_cv, edge='rising')
    def on_reset_rising(self, value, ctx):
        self.x = random.uniform(-1.0, 1.0)
        self.y = random.uniform(-1.0, 1.0)
        self.fx = random.uniform(0.0, 10.0)
        self.fy = random.uniform(0.0, 10.0)
        self.last_time = time.time()

    def main(self, ctx):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        angle = (math.sin(self.x + self.fx) + math.cos(self.y + self.fy)) * self.curl
        vx = math.cos(angle)
        vy = math.sin(angle)
        vx += random.uniform(-1.0, 1.0) * self.noise
        vy += random.uniform(-1.0, 1.0) * self.noise
        mag = math.sqrt(vx * vx + vy * vy) + 1e-09
        vx /= mag
        vy /= mag
        self.x += vx * self.speed * dt
        self.y += vy * self.speed * dt
        self.fx += self.drift * dt * (vx + random.uniform(-0.2, 0.2))
        self.fy += self.drift * dt * (vy + random.uniform(-0.2, 0.2))
        if self.x > 5.0:
            self.x -= 10.0
        elif self.x < -5.0:
            self.x += 10.0
        if self.y > 5.0:
            self.y -= 10.0
        elif self.y < -5.0:
            self.y += 10.0
        yield (self.x, [self.x_cv])
        yield (self.y, [self.y_cv])

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