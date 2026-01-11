from nallely.shifter import *
from nallely import VirtualDevice, VirtualParameter, on


class PitchShifter(VirtualDevice):
    """Pitch shifter
    Shifts a note from -48.0 to +48.0 semitones.
    Semi-tones can be decimal values, input can be also a decimal values, they are quantized later if needed.

    inputs:
    * input_cv [0, 127] <any>: the input note to shift (0-127)
    * shift_cv [-48, 48] init=0 <both>: the amount of shift to apply (-48 to +48)

    outputs:
    * output_cv [0, 127]: the shifted note (0-127)

    type: ondemand
    category: pitch
    """

    input_cv = VirtualParameter(name="input", range=(0.0, 127.0))
    shift_cv = VirtualParameter(name="shift", range=(-48.0, 48.0), default=0.0)

    @on(input_cv, edge="any")
    def shift_input(self, value, ctx):
        if value == 0:
            return 0
        if value > 127:
            return 0
        return value + self.shift

    @property
    def min_range(self):
        return 0.0

    @property
    def max_range(self):
        return 127.0

    @on(shift_cv, edge="both")
    def apply_shift(self, value, ctx):
        if self.input > 0:
            return self.input + value
        return 0
