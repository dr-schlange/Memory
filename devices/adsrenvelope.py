from nallely.eg import *
from nallely import VirtualDevice, VirtualParameter, on

class ADSREnvelope(VirtualDevice):
    """ADSR Envelope Generator

    Simple envelope generator with attack, decay, sustain, release.
    Generates an envelope from a gate:
      - when the gate is up -> triggers the envelope generation
      - when the gate is down -> closes the envelope

    inputs:
    * gate_cv [0, 1] !=0 <rising, falling>: Gate/control voltage input
    * attack_cv [0.0, 1.0] init=0.1: Attack time control in seconds
    * decay_cv [0.0, 1.0] init=0.2: Decay time control in seconds
    * sustain_cv [0.0, 1.0] init=0.7: Sustain level control (0 -> 0%, 1 -> 100%)
    * release_cv [0.0, 1.0] init=0.3: Release time control in seconds

    outputs:
    * output_cv [0, 1]: the generated envelope

    type: continuous
    category: envelope-generator
    """
    gate_cv = VirtualParameter(name='gate', range=(0.0, 1.0), conversion_policy='!=0')
    attack_cv = VirtualParameter(name='attack', range=(0.0, 1.0), default=0.1)
    decay_cv = VirtualParameter(name='decay', range=(0.0, 1.0), default=0.2)
    sustain_cv = VirtualParameter(name='sustain', range=(0.0, 1.0), default=0.7)
    release_cv = VirtualParameter(name='release', range=(0.0, 1.0), default=0.3)

    def __init__(self, attack=0.1, decay=0.2, sustain=0.7, release=0.3, **kwargs):
        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release
        self.gate = 0
        super().__init__(**kwargs)

    @property
    def min_range(self):
        return 0.0

    @property
    def max_range(self):
        return 1.0

    def setup(self):
        ctx = super().setup()
        self._phase = 'idle'
        self._time_in_phase = 0.0
        self._level = 0.0
        self._release_start_level = 0.0
        return ctx

    def debug_print(self, ctx):
        super().debug_print(ctx)
        print(f' * self._phase={self._phase!r}')
        print(f' * self._time_in_phase={self._time_in_phase!r}')
        print(f' * self._level={self._level!r}')

    @on(gate_cv, edge='rising')
    def on_gate_1(self, _, ctx):
        if self._phase in ['idle', 'release']:
            self._phase = 'attack'
            self._time_in_phase = 0.0

    @on(gate_cv, edge='falling')
    def on_gate_0(self, _, ctx):
        if self._phase not in ['release', 'idle']:
            self._phase = 'release'
            self._time_in_phase = 0.0
            self._release_start_level = self._level

    def main(self, ctx):
        dt = self.target_cycle_time
        self._time_in_phase += dt
        if self._phase == 'attack':
            if self.attack == 0:
                self._level = 1.0
                self._phase = 'decay'
                self._time_in_phase = 0.0
            else:
                self._level = min(1.0, self._time_in_phase / self.attack)
                if self._level >= 1.0:
                    self._phase = 'decay'
                    self._time_in_phase = 0.0
        elif self._phase == 'decay':
            if self.decay == 0:
                self._level = self.sustain
                self._phase = 'sustain'
            else:
                decay_progress = self._time_in_phase / self.decay
                self._level = 1.0 - (1.0 - self.sustain) * min(1.0, decay_progress)
                if decay_progress >= 1.0:
                    self._phase = 'sustain'
        elif self._phase == 'sustain':
            self._level = self.sustain
        elif self._phase == 'release':
            if self.release == 0:
                self._level = 0.0
                self._phase = 'idle'
            else:
                release_progress = min(1.0, self._time_in_phase / self.release)
                self._level = self._release_start_level * (1.0 - release_progress)
                if release_progress >= 1.0:
                    self._level = 0.0
                    self._phase = 'idle'
        elif self._phase == 'idle':
            self._level = 0.0
        return self._level

    @property
    def range(self):
        return (0.0, 1.0)