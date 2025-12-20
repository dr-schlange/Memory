from nallely import VirtualDevice, VirtualParameter, on
from nallely import *

class _SuperShifter(VirtualDevice):
    """
    MyDevice

    inputs:
    # * %inname [%range] %options: %doc
    # * io<num>_cv [0, 127]: io, in to write out to read
    * io0_cv [0, 127]: io, in to write out to read
    * io1_cv [0, 127]: io, in to write out to read
    * io2_cv [0, 127]: io, in to write out to read
    * io3_cv [0, 127]: io, in to write out to read
    * trigger_cv [0, 1] >0 <rising>: trigger next step
    * idx_cv [1, 4] round: index sequence

    outputs:
    # * %outname [%range]: %doc

    type: <ondemand | continuous>
    category: <category>
    meta: disable default output
    """
    io0_cv = VirtualParameter(name='io0', range=(0.0, 127.0))
    io1_cv = VirtualParameter(name='io1', range=(0.0, 127.0))
    io2_cv = VirtualParameter(name='io2', range=(0.0, 127.0))
    io3_cv = VirtualParameter(name='io3', range=(0.0, 127.0))
    trigger_cv = VirtualParameter(name='trigger', range=(0.0, 1.0), conversion_policy='>0')
    idx_cv = VirtualParameter(name='idx', range=(1.0, 4.0), conversion_policy='round')

    def __post_init__(self, **kwargs):
        return {'disable_output': True}

    @on(trigger_cv, edge='rising')
    def on_trigger_rising(self, value, ctx):
        value = getattr(self, f'io{int(self.idx)}')
        yield (0, [getattr(self, f'io{int(self.idx)}_cv')])
        if self.idx >= 3:
            self.idx = 0
        else:
            self.idx += 1
        yield (value, [getattr(self, f'io{int(self.idx)}_cv')])