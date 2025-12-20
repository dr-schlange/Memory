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
    * idx_cv [0, 7] round: index sequence
    * io4_cv [0, 127]: io, in to write out to read
    * io5_cv [0, 127]: io, in to write out to read
    * io6_cv [0, 127]: io, in to write out to read
    * io7_cv [0, 127]: io, in to write out to read
    * length_cv [1, 8] init=8 round: length sequence

    outputs:
    # * %outname [%range]: %doc

    type: <ondemand | continuous>
    category: <category>
    meta: disable default output
    """
    io4_cv = VirtualParameter(name='io4', range=(0.0, 127.0))
    io5_cv = VirtualParameter(name='io5', range=(0.0, 127.0))
    io6_cv = VirtualParameter(name='io6', range=(0.0, 127.0))
    io7_cv = VirtualParameter(name='io7', range=(0.0, 127.0))
    length_cv = VirtualParameter(name='length', range=(1.0, 8.0), conversion_policy='round', default=8.0)
    io0_cv = VirtualParameter(name='io0', range=(0.0, 127.0))
    io1_cv = VirtualParameter(name='io1', range=(0.0, 127.0))
    io2_cv = VirtualParameter(name='io2', range=(0.0, 127.0))
    io3_cv = VirtualParameter(name='io3', range=(0.0, 127.0))
    trigger_cv = VirtualParameter(name='trigger', range=(0.0, 1.0), conversion_policy='>0')
    idx_cv = VirtualParameter(name='idx', range=(0.0, 7.0), conversion_policy='round')

    def __post_init__(self, **kwargs):
        return {'disable_output': True}

    @on(trigger_cv, edge='rising')
    def on_trigger_rising(self, value, ctx):
        prev = (self.idx - 1) % self.length
        pvalue = getattr(self, f'io{int(prev)}')
        value = getattr(self, f'io{int(self.idx)}')
        yield (pvalue, [getattr(self, f'io{int(self.idx)}_cv')])
        if self.idx < 1:
            self.idx = self.length
        self.idx -= 1
        yield (value, [getattr(self, f'io{int(self.idx)}_cv')])