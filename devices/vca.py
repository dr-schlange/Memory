import math
from nallely.eg import *
from nallely import VirtualDevice, VirtualParameter, on

class VCA(VirtualDevice):
    """Voltage Controled Amplifier

    Simple VCA implementation with gain

    inputs:
    * input_cv [0, 127] <any>: Input signal
    * amplitude_cv [0.0, 1.0] init=0.0 <any>: Signal amplitude (0.0 -> 0%, 1.0 -> 100%)
    * gain_cv [1.0, 2.0] init=1.0: Signal gain (default is 1.0)

    outputs:
    * output_cv [0, 127]: The amplified signal

    type: ondemand
    category: amplitude-modulation
    """
    input_cv = VirtualParameter(name='input', range=(0.0, 127.0))
    amplitude_cv = VirtualParameter(name='amplitude', range=(0.0, 1.0), default=0.0)
    gain_cv = VirtualParameter(name='gain', range=(1.0, 2.0), default=1.0)
    output_cv = VirtualParameter(name='output', range=(0.0, 127.0))

    @property
    def min_range(self):
        return 0.0

    @property
    def max_range(self):
        return 127.0

    @on(input_cv, edge='any')
    def sending_modulated_input(self, value, ctx):
        if self.input > 0.2:
            return value * math.exp(self.amplitude * self.gain)
        return 0

    @on(amplitude_cv, edge='any')
    def change_amplitude(self, value, ctx):
        if self.input > 0.1:
            return self.input * math.exp(self.amplitude * self.gain)
        return 0