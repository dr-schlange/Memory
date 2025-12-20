from collections import deque
from typing import Any
from nallely.core.world import ThreadContext
from nallely import VirtualDevice, VirtualParameter, on
from nallely import *

class DownScaler(VirtualDevice):
    """
    DownScaler

    Splits a signal in 2 outputs, distributing alternating between the various outputs.

    inputs:
    * input_cv [0, 127] init=0 <any>: The input signal

    outputs:
    * out0_cv [0, 127]: First downscaled version
    * out1_cv [0, 127]: Second downscaled version

    type: ondemand
    category: <category>
    meta: disable default output
    """
    input_cv = VirtualParameter(name='input', range=(0.0, 127.0), default=0.0)
    out1_cv = VirtualParameter(name='out1', range=(0.0, 127.0))
    out0_cv = VirtualParameter(name='out0', range=(0.0, 127.0))

    def __post_init__(self, **kwargs):
        self.idx = 1
        self.outs = [self.out0_cv, self.out1_cv]
        return {'disable_output': True}

    @on(input_cv, edge='any')
    def on_input_any(self, value, ctx):
        self.idx = (self.idx + 1) % 2
        return (value, [self.outs[self.idx]])