import bisect
import math
import random
from decimal import Decimal
from nallely import VirtualDevice, VirtualParameter, on
from nallely import *

class FineTuneNote(VirtualDevice):
    """
    FineTuneNote

    inputs:
    # * %inname [%range] %options: %doc
    * input_cv [0, 127] <any>: main input
    * slide_cv [0, 1] init=1 >0: if activated each pitch variation will not produce a new note on
    * finetune_cv [0, 8191] init=2048 round <any>: fine tune how the conversion for fraction should be handled (depends on your synth/preset)

    outputs:
    # * %outname [%range]: %doc
    * note_out_cv [0, 127]: main note output (connect to the key of the synth)
    * pitchwheel_out_cv [-8192, 8191]: main fine-tuned note (connect to the pitchwheel of the synth)

    type: <ondemand | continuous>
    cateory: <category>
    meta: disable default output
    """
    finetune_cv = VirtualParameter(name='finetune', range=(0.0, 8191.0), conversion_policy='round', default=2048.0)
    slide_cv = VirtualParameter(name='slide', range=(0.0, 1.0), conversion_policy='>0', default=1.0)
    input_cv = VirtualParameter(name='input', range=(0.0, 127.0))
    pitchwheel_out_cv = VirtualParameter(name='pitchwheel_out', range=(-8192.0, 8191.0))
    note_out_cv = VirtualParameter(name='note_out', range=(0.0, 127.0))

    def __post_init__(self, **kwargs):
        return {'disable_output': True}

    @on(input_cv, edge='any')
    def on_input_any(self, value, ctx):
        closest_note, fine_tune = divmod(value, 1.0)
        pitchwheel = round(fine_tune * self.finetune)
        if not self.slide:
            yield (0, [self.note_out_cv])
        yield (closest_note, [self.note_out_cv])
        yield (pitchwheel, [self.pitchwheel_out_cv])

    @on(finetune_cv, edge='any')
    def on_finetune_any(self, value, ctx):
        closest_note, fine_tune = divmod(self.input, 1.0)
        pitchwheel = round(fine_tune * value)
        yield (closest_note, [self.note_out_cv])
        yield (pitchwheel, [self.pitchwheel_out_cv])