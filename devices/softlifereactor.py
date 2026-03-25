from mydevice import *
from nallely import VirtualDevice, VirtualParameter, on
from nallely.codegen import gencode
import random
import time
import math

@gencode(keep_decorator=True)
class SoftLifeReactor(VirtualDevice):
    """Soft Life Reactor

    A continuous, life-like generative system inspired by
    cellular automata, reaction–diffusion, and neural fields.
    Instead of discrete rules, the system evolves via smooth
    growth, decay, and neighborhood interaction.

    The output represents the moving center of activity of
    the living field and produces emergent 2D patterns
    resembling gliders, blobs, and oscillators.

    inputs:
    * growth_cv [0.0, 2.0] init=1.0:
        strength of local excitation
    * decay_cv [0.0, 1.0] init=0.2:
        global energy loss
    * spread_cv [0.0, 1.0] init=0.3:
        diffusion between neighbors
    * noise_cv [0.0, 0.5] init=0.05:
        stochastic mutation
    * reset_cv [0, 1] round <rising>:
        reseed the life field

    outputs:
    * x_cv [-5.0, 5.0]:
        activity center x
    * y_cv [-5.0, 5.0]:
        activity center y

    type: hybrid
    category: generative
    """
    growth_cv = VirtualParameter(name='growth', range=(0.0, 2.0), default=1.0)
    decay_cv = VirtualParameter(name='decay', range=(0.0, 1.0), default=0.2)
    spread_cv = VirtualParameter(name='spread', range=(0.0, 1.0), default=0.3)
    noise_cv = VirtualParameter(name='noise', range=(0.0, 0.5), default=0.05)
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')
    x_cv = VirtualParameter(name='x', range=(-5.0, 5.0))
    y_cv = VirtualParameter(name='y', range=(-5.0, 5.0))

    def __post_init__(self, **kwargs):
        self.size = 16
        self.field = [[random.random() * 0.2 for _ in range(self.size)] for _ in range(self.size)]
        self.last_time = time.time()

    @on(reset_cv, edge='rising')
    def on_reset(self, value, ctx):
        for y in range(self.size):
            for x in range(self.size):
                self.field[y][x] = random.random() * 0.2
        self.last_time = time.time()

    def main(self, ctx):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        new_field = [[0.0 for _ in range(self.size)] for _ in range(self.size)]
        total_energy = 0.0
        cx = 0.0
        cy = 0.0
        for y in range(self.size):
            for x in range(self.size):
                a = self.field[y][x]
                n = 0.0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx = (x + dx) % self.size
                        ny = (y + dy) % self.size
                        n += self.field[ny][nx]
                n /= 8.0
                growth = math.exp(-(n - 0.35) ** 2 * 12.0)
                da = self.growth * growth - self.decay * a
                a_new = a + da * dt
                a_new += (n - a) * self.spread * dt
                a_new += random.uniform(-1.0, 1.0) * self.noise * dt
                a_new = max(0.0, min(1.0, a_new))
                new_field[y][x] = a_new
                total_energy += a_new
                cx += x * a_new
                cy += y * a_new
        self.field = new_field
        if total_energy > 1e-06:
            cx /= total_energy
            cy /= total_energy
        x_out = cx / self.size * 10.0 - 5.0
        y_out = cy / self.size * 10.0 - 5.0
        yield (x_out, [self.x_cv])
        yield (y_out, [self.y_cv])

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