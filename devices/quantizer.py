from nallely.shifter import *
from nallely import VirtualDevice, VirtualParameter, on


class Quantizer(VirtualDevice):
    input_cv = VirtualParameter("input", range=(0, 127))
    trigger_cv = VirtualParameter("trigger", range=(0, 1), conversion_policy="round")
    reset_cv = VirtualParameter("reset", range=(0, 1))
    root_cv = VirtualParameter("root", accepted_values=NOTE_NAMES, disable_policy=True)
    scale__cv = VirtualParameter(
        "scale_", accepted_values=tuple(SCALE_INTERVALS.keys()), disable_policy=True
    )
    type_cv = VirtualParameter("type", accepted_values=("sample&hold", "free"))

    def __init__(self, **kwargs):
        self.input = 0
        self.root = self.root_cv.parameter.accepted_values[0]
        self.scale_ = self.scale__cv.parameter.accepted_values[0]
        self.type = self.type_cv.parameter.accepted_values[0]
        self.trigger = 0
        self.reset = 0
        self.hold = None
        self.update_nearest_table(NOTES[self.root], SCALES[self.scale_])
        super().__init__(**kwargs)

    def store_input(self, param: str, value):
        if param == "root":
            accepted_values = self.root_cv.parameter.accepted_values
            if isinstance(value, (int, float, Decimal)):
                value = accepted_values[int(value % 12)]
            self.update_nearest_table(NOTES[value], SCALES[self.scale_])
        elif param == "scale_":
            accepted_values = self.scale__cv.parameter.accepted_values
            if isinstance(value, (int, float, Decimal)):
                value = accepted_values[int(value % len(accepted_values))]
            self.update_nearest_table(NOTES[self.root], SCALES[value])
        elif param == "trigger" or param == "reset":
            value = 1 if value > 0 else 0
        return super().store_input(param, value)

    @staticmethod
    def nearest_note(relative_note, scale_instance):
        i = bisect.bisect_left(scale_instance, relative_note)
        if i == 0:
            return scale_instance[0]
        if i == len(scale_instance):
            return scale_instance[-1]
        before = scale_instance[i - 1]
        after = scale_instance[i]
        if abs(after - relative_note) < abs(relative_note - before):
            return after
        return before

    def update_nearest_table(self, root, scale_instance):
        shifted_scale = [(n + root) % 12 for n in scale_instance]
        self.table = [self.nearest_note(pc, shifted_scale) for pc in range(12)]

    def snap_to_scale(self, note):
        note = int(note)
        octave = note // 12
        return self.table[note % 12] + 12 * octave

    @on(input_cv, edge="any")
    def convert_note(self, value, ctx):
        if self.type == "sample&hold":
            return
        return self.snap_to_scale(value)

    @on(trigger_cv, edge="rising")
    def trigger_sample(self, value, ctx):
        if self.type == "sample&hold":
            self.hold = self.snap_to_scale(self.input)
            return self.hold

    @on(reset_cv, edge="rising")
    def reset_input(self, value, ctx):
        yield self.hold
        self.hold = None
