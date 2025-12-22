from nallely import VirtualDevice, VirtualParameter, on
from nallely import *

class _StreetFighter(VirtualDevice):
    """
    MyDevice

    inputs:
    # * %inname [%range] %options: %doc
    * hadoken_cv [0, 1] >0 <rising>: had
    * shoryuken_cv [0, 1] >0 <rising>: shoryuken

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
    shoryuken_cv = VirtualParameter(name='shoryuken', range=(0.0, 1.0), conversion_policy='>0')
    shoryulen_cv = VirtualParameter(name='shoryulen', range=(0.0, 1.0), conversion_policy='>0')
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
        self.delay = 50
        return {'disable_output': True}

    def combine(self, combination):
        for key in combination:
            yield (1, [getattr(self, f'{key}_cv')])
            yield from self.sleep(self.delay)
            yield (0, [getattr(self, f'{key}_cv')])
            yield from self.sleep(self.delay)

    @on(hadoken_cv, edge='rising')
    def on_hadoken_rising(self, value, ctx):
        yield from self.combine(['down', 'right', 'b'])

    @on(shoryulen_cv, edge='rising')
    def on_shoryulen_rising(self, value, ctx):
        yield from self.combine(['right', 'down', 'right', 'b'])

    @on(shoryuken_cv, edge='rising')
    def on_shoryuken_rising(self, value, ctx):
        ...