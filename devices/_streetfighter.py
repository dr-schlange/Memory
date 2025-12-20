from nallely import VirtualDevice, VirtualParameter, on
from nallely import *

class _StreetFighter(VirtualDevice):
    """
    MyDevice

    inputs:
    # * %inname [%range] %options: %doc
    * hadoken_cv [0, 1] >0 <rising>: had

    outputs:
    # * %outname [%range]: %doc
    * a_cv [0, 1]: a output
    * b_cv [0, 1]: b output
    * _start_cv [0, 1]: start output
    * select_cv [0, 1]: select output
    * up_cv [0, 1]: up output
    * down_cv [0, 1]: down output
    * left_cv [0, 1]: left output
    * right_cv [0, 1]: right output 

    $$
    trig: yield 1, [self.<port>_cv]
    yield 0, [self.<port>_cv]
    $$

    type: <ondemand | continuous>
    category: <category>
    meta: disable default output
    """
    hadoken_cv = VirtualParameter(name='hadoken', range=(0.0, 1.0), conversion_policy='>0')
    right_cv = VirtualParameter(name='right', range=(0.0, 1.0))
    left_cv = VirtualParameter(name='left', range=(0.0, 1.0))
    down_cv = VirtualParameter(name='down', range=(0.0, 1.0))
    up_cv = VirtualParameter(name='up', range=(0.0, 1.0))
    select_cv = VirtualParameter(name='select', range=(0.0, 1.0))
    _start_cv = VirtualParameter(name='_start', range=(0.0, 1.0))
    b_cv = VirtualParameter(name='b', range=(0.0, 1.0))
    a_cv = VirtualParameter(name='a', range=(0.0, 1.0))

    def __post_init__(self, **kwargs):
        return {'disable_output': True}

    @on(hadoken_cv, edge='rising')
    def on_hadoken_rising(self, value, ctx):
        yield (1, [self.down_cv])
        yield (0, [self.down_cv])
        yield (1, [self.right_cv])
        yield (0, [self.right_cv])
        yield (1, [self.a_cv])
        yield (0, [self.a_cv])