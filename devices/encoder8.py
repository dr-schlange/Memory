from nallely import VirtualDevice, VirtualParameter, on

class Encoder8(VirtualDevice):
    """
    MyDevice

    inputs:
    # * %inname [%range] %options: %doc
    # %options
    * resolution_cv [0, 50] init=1.14 <any>: Parameter description
    * inx_cv [0, 7] init=4 round <any>: Parameter description
    * iny_cv [0, 7] init=4 round <any>: Parameter description
    * reset_cv [0, 1] round <rising>: doc

    outputs:
    # * %outname [%range]: %doc
    * x_cv [0, 7]: out8
    * y_cv [0, 7]: out8

    type: dehybrid
    category: <category>
    # meta: disable default output
    """
    reset_cv = VirtualParameter(name='reset', range=(0.0, 1.0), conversion_policy='round')
    inx_cv = VirtualParameter(name='inx', range=(0.0, 7.0), conversion_policy='round', default=4.0)
    iny_cv = VirtualParameter(name='iny', range=(0.0, 7.0), conversion_policy='round', default=4.0)
    resolution_cv = VirtualParameter(name='resolution', range=(0.0, 50.0), default=1.14)
    y_cv = VirtualParameter(name='y', range=(0.0, 7.0))
    x_cv = VirtualParameter(name='x', range=(0.0, 7.0))
    out_cv = VirtualParameter(name='out', range=(0.0, 4.0))

    @on(resolution_cv, edge='any')
    def on_resolution_any(self, value, ctx):
        ...

    def __post_init__(self, **kwargs):
        self.image = [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]]

    def main(self, ctx):
        image = self.image
        for y in range(-1, -len(image), -1):
            for x in range(len(image)):
                if image[y][x]:
                    yield (x, [self.x_cv])
                    yield (-y, [self.y_cv])
                yield from self.sleep(self.resolution)

    @on(iny_cv, edge='any')
    def on_iny_any(self, value, ctx):
        val = self.image[int(value)][int(self.inx)]
        self.image[int(value)][int(self.inx)] = int(not bool(int(value)))

    @on(inx_cv, edge='any')
    def on_inx_any(self, value, ctx):
        val = self.image[int(self.iny)][int(value)]
        self.image[int(self.iny)][int(value)] = int(not bool(int(val)))

    @on(reset_cv, edge='rising')
    def on_reset_rising(self, value, ctx):
        self.__post_init__()
