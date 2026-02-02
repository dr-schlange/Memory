from mydevice import *
import time
import math
import random
from nallely import VirtualDevice, VirtualParameter, on
from nallely.codegen import gencode

@gencode(keep_decorator=True)
class SchrodingerNeuron(VirtualDevice):
    """Schrödinger Equation Neuron (Non-Relativistic)

    Simulates a local time-dependent Schrödinger equation
    with a complex wavefunction evolving under an external
    potential.
    """
    potential_cv = VirtualParameter(name='potential', range=(-10.0, 10.0), default=0.0)
    mass_cv = VirtualParameter(name='mass', range=(0.1, 10.0), default=1.0)
    hbar_cv = VirtualParameter(name='hbar', range=(0.01, 2.0), default=1.0)
    observe_cv = VirtualParameter(name='observe', range=(0.0, 1.0), conversion_policy='round')
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')

    @property
    def min_range(self):
        return -1.0

    @property
    def max_range(self):
        return 1.0

    def __post_init__(self, **kwargs):
        angle = random.uniform(0, 2 * math.pi)
        self.psi_real = math.cos(angle)
        self.psi_imag = math.sin(angle)
        self.last_time = time.time()

    @on(reset_cv, edge='rising')
    def on_reset(self, value, ctx):
        angle = random.uniform(0, 2 * math.pi)
        self.psi_real = math.cos(angle)
        self.psi_imag = math.sin(angle)
        self.last_time = time.time()

    @on(observe_cv, edge='rising')
    def on_observe(self, value, ctx):
        prob = self.psi_real ** 2 + self.psi_imag ** 2
        sign = 1.0 if random.random() < 0.5 else -1.0
        self.psi_real = sign * math.sqrt(prob)
        self.psi_imag = 0.0

    def main(self, ctx):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now
        V = self.potential
        hbar = max(self.hbar, 1e-06)
        d_real = V / hbar * self.psi_imag * dt
        d_imag = -(V / hbar) * self.psi_real * dt
        self.psi_real += d_real
        self.psi_imag += d_imag
        norm = math.sqrt(self.psi_real ** 2 + self.psi_imag ** 2)
        if norm > 0:
            self.psi_real /= norm
            self.psi_imag /= norm
        prob = self.psi_real ** 2 + self.psi_imag ** 2
        return self.psi_real