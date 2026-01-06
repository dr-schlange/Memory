from nallely.experimental.maths import *
from nallely import VirtualDevice, VirtualParameter, on


class UniversalSlopeGenerator(VirtualDevice):
    """UniversalSlopeGenerator

    Serge-inspired Universal Slope Generator (single channel).

    Generates voltage-controlled slopes for:
    - AD / AR envelopes
    - Cycling LFOs
    - Slew limiting
    - Trigger-to-envelope generation
    - Free-running function generation

    Hybrid operation:
    - Reactive when externally triggered
    - Continuous when cycle enabled

    NOTE: This module is LLM generated

    inputs:
    * trig_cv [0, 1] >0 <rising>: Rising-edge trigger input. Starts a new slope immediately.
    * gate_cv [0, 1] >0 <rising, falling>: Gate input. Rising edge begins rise phase; falling edge begins fall phase.
    * rise_cv [0.001, 10.0]: Rise time control. Exponential response.
    * fall_cv [0.001, 10.0]: Fall time control. Exponential response.
    * shape_cv [log, lin, exp]: Curve mode for both rise and fall.
    * cycle_cv [off, on] <any>: Cycle enable. When non-zero, slope free-runs continuously,
                           restarting automatically after EOC.
    * reset_cv [0, 1] >0 <rising>: Immediate reset. Forces output to 0 and stops the slope.

    outputs:
    * out_cv [0, 1]: Main slope output.
    * inv_cv [0, 1]: Inverted output (1 - out).
    * eor_cv [0, 1]: End Of Rise pulse. Emits a short pulse at the end of the rise phase.
    * eoc_cv [0, 1]: End Of Cycle pulse. Emits a short pulse at the end of the fall phase.

    type: hybrid
    category: function-generator
    meta: disable default output
    """

    gate_cv = VirtualParameter(name="gate", range=(0.0, 1.0), conversion_policy=">0")
    rise_cv = VirtualParameter(name="rise", range=(0.001, 10.0))
    fall_cv = VirtualParameter(name="fall", range=(0.001, 10.0))
    shape_cv = VirtualParameter(name="shape", accepted_values=["log", "lin", "exp"])
    cycle_cv = VirtualParameter(name="cycle", accepted_values=["off", "on"])
    reset_cv = VirtualParameter(name="reset", range=(0.0, 1.0), conversion_policy=">0")
    trig_cv = VirtualParameter(name="trig", range=(0.0, 1.0), conversion_policy=">0")
    eoc_cv = VirtualParameter(name="eoc", range=(0.0, 1.0))
    eor_cv = VirtualParameter(name="eor", range=(0.0, 1.0))
    inv_cv = VirtualParameter(name="inv", range=(0.0, 1.0))
    out_cv = VirtualParameter(name="out", range=(0.0, 1.0))

    def __post_init__(self, **kwargs):
        self.phase = "idle"
        self.value = 0.0
        self.eor_pulse = 0.0
        self.eoc_pulse = 0.0
        self.last_time = time.time()
        return {"disable_output": True}

    def _apply_shape(self, t: float, shape: str) -> float:
        """Apply curve shaping to a normalized t [0,1]"""
        if shape == "lin":
            return t
        elif shape == "exp":
            return t**2
        elif shape == "log":
            return math.sqrt(t)
        return t

    def _advance_phase(self):
        """Update slope value and yield outputs (including pulses)."""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        if self.phase == "idle":
            yield (self.value, [self.out_cv])
            yield (1.0 - self.value, [self.inv_cv])
            return
        if self.phase == "rising":
            rate = max(self.rise, 0.001)
            remaining = 1.0 - self.value
        elif self.phase == "falling":
            rate = max(self.fall, 0.001)
            remaining = self.value
        else:
            return
        if self.shape == "lin":
            delta = dt / rate
        elif self.shape == "exp":
            delta = remaining * dt / rate
        elif self.shape == "log":
            delta = remaining**0.5 * dt / rate
        else:
            delta = dt / rate
        pulse = None
        if self.phase == "rising":
            self.value += delta
            if self.value >= 1.0:
                self.value = 1.0
                pulse = ("eor", self.eor_cv)
                if self.gate != 0:
                    self.phase = "falling"
        elif self.phase == "falling":
            self.value -= delta
            if self.value <= 0.0:
                self.value = 0.0
                pulse = ("eoc", self.eoc_cv)
                self.phase = "idle"
        if pulse:
            channel, output = pulse
            yield (1.0, [output])
            yield (0.0, [output])
            if channel == "eoc" and self.cycle == "on":
                self.phase = "rising"
                self.value = 0.0
        self.value = max(0.0, min(1.0, self.value))
        yield (self.value, [self.out_cv])
        yield (1.0 - self.value, [self.inv_cv])

    def main(self, ctx: ThreadContext):
        yield from self._advance_phase()

    @on(trig_cv, edge="rising")
    def on_trig_rising(self, value, ctx):
        self.phase = "rising"
        self.value = 0.0
        return (self.value, [self.out_cv])

    @on(reset_cv, edge="rising")
    def on_reset_rising(self, value, ctx):
        self.phase = "idle"
        self.value = 0.0
        self.eor_pulse = 0.0
        self.eoc_pulse = 0.0
        return (0.0, [self.out_cv, self.inv_cv, self.eor_cv, self.eoc_cv])

    @on(gate_cv, edge="rising")
    def on_gate_rising(self, value, ctx):
        self.phase = "rising"

    @on(gate_cv, edge="falling")
    def on_gate_falling(self, value, ctx):
        self.phase = "falling"

    @on(cycle_cv, edge="any")
    def on_cycle_any(self, value, ctx):
        if value == "on" and self.phase == "idle":
            self.phase = "rising"
            self.value = 0.0
