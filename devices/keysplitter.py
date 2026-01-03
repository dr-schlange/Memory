from collections import deque
from typing import Any
from nallely.core.world import ThreadContext
from nallely import VirtualDevice, VirtualParameter, on
from nallely import *


class KeySplitter(VirtualDevice):
    """KeySplitter

    Let's you route notes depending on ranges

    inputs:
    # * %inname [%range] %options: %doc
    * input_cv [0, 127] <any>: input notes
    * range0_cv [0, 127] init=34: threshold for first note
    * range1_cv [0, 127] init=64: threshold for second note
    * range2_cv [0, 127] init=94: threshold for third note
    * mode_cv [exclusive, keeplast]: should the module cut the last value of each range

    outputs:
    # * %outname [%range]: %doc
    * out0_cv [0, 127]: note output
    * out1_cv [0, 127]: note output
    * out2_cv [0, 127]: note output
    * out3_cv [0, 127]: note output

    type: <ondemand | continuous>
    category: <category>
    meta: disable default output
    """

    mode_cv = VirtualParameter(name="mode", accepted_values=["exclusive", "keeplast"])
    input_cv = VirtualParameter(name="input", range=(0.0, 127.0))
    range0_cv = VirtualParameter(name="range0", range=(0.0, 127.0), default=34.0)
    range1_cv = VirtualParameter(name="range1", range=(0.0, 127.0), default=64.0)
    range2_cv = VirtualParameter(name="range2", range=(0.0, 127.0), default=94.0)
    out3_cv = VirtualParameter(name="out3", range=(0.0, 127.0))
    out2_cv = VirtualParameter(name="out2", range=(0.0, 127.0))
    out1_cv = VirtualParameter(name="out1", range=(0.0, 127.0))
    out0_cv = VirtualParameter(name="out0", range=(0.0, 127.0))

    def __post_init__(self, **kwargs):
        return {"disable_output": True}

    @on(input_cv, edge="any")
    def on_input_any(self, value, ctx):
        val = ctx.raw_value
        if 0 < val <= self.range0:
            yield (val, [self.out0_cv])
            output = 0
        if self.range0 < val <= self.range1:
            yield (val, [self.out1_cv])
            output = 1
        if self.range1 < val <= self.range2:
            yield (val, [self.out2_cv])
            output = 2
        if self.range2 < val <= 127:
            yield (val, [self.out3_cv])
            output = 3
        if self.mode == "exclusive":
            return (0, [getattr(self, f"out{i}_cv") for i in range(4) if i != output])
