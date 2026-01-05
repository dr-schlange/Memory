from mydevice import *
from nallely import VirtualDevice, VirtualParameter, on


class _ExpA(VirtualDevice):
    """
    MyDevice

    inputs:
    # * %inname [%range] %options: %doc
    * input_cv [0, 127] <any>: input
    * trigger_cv [0, 1] >0 <rising>: trig

    outputs:
    # * %outname [%range]: %doc

    type: <ondemand | continuous>
    category: <category>
    # meta: disable default output
    """

    trigger_cv = VirtualParameter(
        name="trigger", range=(0.0, 1.0), conversion_policy=">0"
    )
    input_cv = VirtualParameter(name="input", range=(0.0, 127.0))

    def __post_init__(self, **kwargs): ...

    def creating(self):
        from nallely.experimental.maths import UniversalSlopeGenerator

        child = UniversalSlopeGenerator()
        self.output_cv = child
        child.start()
        self.child = child

    @on(input_cv, edge="any")
    def on_input_any(self, value, ctx):
        self.creating()

    @on(VirtualDevice.output_cv, edge="any")
    def on_output_any(self, value, ctx):
        return value

    @on(trigger_cv, edge="rising")
    def on_trigger_rising(self, value, ctx): ...
