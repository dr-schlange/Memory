from nallely import VirtualDevice, VirtualParameter, on
from nallely import *

class _Zab(VirtualDevice):
    """
    MyDevice

    inputs:
    # * %inname [%range] %options: %doc
    * io0_cv [0, 127] round <increase, decrease>: first io
    * io1_cv [0, 127] round <increase, decrease>: io
    * in2_cv [0, 127] round <increase, decrease>: Parameter description
    * incr_cv [0, 127] round <increase>: Parameter description
    * decr_cv [0, 127] round <decrease>: Parameter description

    outputs:
    # * %outname [%range]: %doc

    type: <ondemand | continuous>
    category: <category>
    # meta: disable default output
    """
    io0_cv = VirtualParameter(name='io0', range=(0.0, 127.0), conversion_policy='round')
    io1_cv = VirtualParameter(name='io1', range=(0.0, 127.0), conversion_policy='round')
    in2_cv = VirtualParameter(name='in2', range=(0.0, 127.0), conversion_policy='round')
    incr_cv = VirtualParameter(name='incr', range=(0.0, 127.0), conversion_policy='round')
    decr_cv = VirtualParameter(name='decr', range=(0.0, 127.0), conversion_policy='round')

    @on(decr_cv, edge='decrease')
    def on_decr_decrease(self, value, ctx):
        yield (value, [self.decr_cv])

    @on(incr_cv, edge='increase')
    def on_incr_increase(self, value, ctx):
        yield (value, [self.incr_cv])

    @on(in2_cv, edge='increase')
    def on_in2_increase(self, value, ctx):
        yield (value, [self.in2_cv])

    @on(in2_cv, edge='decrease')
    def on_in2_decrease(self, value, ctx):
        yield (value, [self.in2_cv])

    @on(io1_cv, edge='increase')
    def on_io1_increase(self, value, ctx):
        yield (value, [self.io1_cv])

    @on(io1_cv, edge='decrease')
    def on_io1_decrease(self, value, ctx):
        yield (value, [self.io1_cv])

    @on(io0_cv, edge='increase')
    def on_io0_increase(self, value, ctx):
        yield (value, [self.io0_cv])

    @on(io0_cv, edge='decrease')
    def on_io0_decrease(self, value, ctx):
        yield (value, [self.io0_cv])