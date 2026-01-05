from _expa import *
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

        usg = UniversalSlopeGenerator()
        usg.trig_cv = usg.eoc_cv
        self.output_cv = usg.out_cv
        usg.start()
        usg.set_parameter("gate", 1)
        usg.rise = 0.204
        usg.fall = 0.504
        yield from self.sleep(10)
        self.usg = usg

    @on(input_cv, edge="any")
    def on_input_any(self, value, ctx):
        pass

    @on(VirtualDevice.output_cv, edge="any")
    def on_output_any(self, value, ctx):
        return value

    @on(trigger_cv, edge="rising")
    def on_trigger_rising(self, value, ctx):
        yield from self.creating()
