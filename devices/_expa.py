from mydevice import *
from nallely import VirtualDevice, VirtualParameter, on


class _ExpA(VirtualDevice):
    """
    MyDevice

    inputs:
    # * %inname [%range] %options: %doc
    * input_cv [0, 1270, 127] <any>: input

    outputs:
    # * %outname [%range]: %doc

    type: <ondemand | continuous>
    category: <category>
    meta: disable default output
    """

    input_cv = VirtualParameter(name="input", range=(0.0, 1270.0))

    def __post_init__(self, **kwargs):
        return {"disable_output": True}

    @on(input_cv, edge="any")
    def on_input_any(self, value, ctx): ...
