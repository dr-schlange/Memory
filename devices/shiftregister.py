from nallely.switchs import *
from nallely import VirtualDevice, VirtualParameter, on


class ShiftRegister(VirtualDevice):
    input_cv = VirtualParameter("input", range=(0, 127))
    trigger_cv = VirtualParameter("trigger", range=(0, 1), conversion_policy="round")
    reset_cv = VirtualParameter("reset", range=(0, 1))
    length_cv = VirtualParameter(
        "length", range=(2, 8), conversion_policy="round", default=8
    )
    output7_cv = VirtualParameter("output7", range=(0, 127))
    output6_cv = VirtualParameter("output6", range=(0, 127))
    output5_cv = VirtualParameter("output5", range=(0, 127))
    output4_cv = VirtualParameter("output4", range=(0, 127))
    output3_cv = VirtualParameter("output3", range=(0, 127))
    output2_cv = VirtualParameter("output2", range=(0, 127))
    output1_cv = VirtualParameter("output1", range=(0, 127))
    output0_cv = VirtualParameter("output0", range=(0, 127))

    def __init__(self, **kwargs):
        self.input = 0
        self.trigger = 0
        self.reset = 0
        self.length = 8
        self.registers: deque[int | None] = deque([None] * 8, maxlen=8)
        self.outputs = [None] * 8
        for i in range(8):
            setattr(self, f"output{i}", 0)
            self.outputs[i] = getattr(self, f"output{i}_cv")
        super().__init__(disable_output=True, **kwargs)

    @on(trigger_cv, edge="rising")
    def trigger_next_step(self, value, ctx):
        self.registers.appendleft(self.input)
        for i, (register, output) in enumerate(
            zip(list(self.registers)[: self.length], self.outputs[: self.length])
        ):
            if register is not None:
                yield (register, [output])

    @on(reset_cv, edge="rising")
    def reset_values(self, value, ctx):
        for i in range(8):
            self.registers[i] = None
        yield (0, self.outputs)
