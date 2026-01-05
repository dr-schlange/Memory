from nallely.newmodule import *
from nallely import VirtualDevice, VirtualParameter, on
from nallely import *


class MyDevice(VirtualDevice):
    """
    MyDevice

    inputs:
    # * %inname [%range] %options: %doc

    outputs:
    # * %outname [%range]: %doc

    type: <ondemand | continuous>
    category: <category>
    # meta: disable default output
    """
