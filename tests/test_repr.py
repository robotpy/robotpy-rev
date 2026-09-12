import pytest

import rev

STRUCT_TYPES = [
    rev.SparkBase.Faults,
    rev.SparkBase.Warnings,
    rev.DetachedEncoder.Faults,
    rev.ServoHub.Faults,
    rev.ServoHub.Warnings,
    rev.A301.FirmwareVersion,
    rev.A301.Faults,
    rev.A301.Warnings,
    rev.ServoChannelConfig.PulseRange_t,
    *[getattr(rev.SparkLowLevel, f"PeriodicStatus{i}") for i in range(10)],
    rev.DetachedEncoderLowLevel.FirmwareVersion,
    *[getattr(rev.DetachedEncoderLowLevel, f"PeriodicStatus{i}") for i in range(5)],
    rev.ServoHubLowLevel.FirmwareVersion,
    *[getattr(rev.ServoHubLowLevel, f"PeriodicStatus{i}") for i in range(5)],
]


@pytest.mark.parametrize("cls", STRUCT_TYPES, ids=lambda cls: cls.__qualname__)
def test_struct_repr_includes_all_fields_and_current_values(cls):
    fields = [name for name, attr in vars(cls).items() if isinstance(attr, property)]
    # Change one field at a time to catch swapped boolean arguments as well.
    for changed_field in (None, *fields):
        value = cls()
        expected = {}
        for index, name in enumerate(fields, 1):
            current = getattr(value, name)
            if name == changed_field:
                if isinstance(current, bool):
                    current = not current
                elif isinstance(current, float):
                    current = index + 0.25
                elif isinstance(current, int):
                    current = index
                else:
                    current = list(type(current).__members__.values())[-1]
                setattr(value, name, current)
            expected[name] = repr(current)

        result = repr(value)
        assert result.startswith(f"{cls.__qualname__}(")
        assert result.endswith(")")
        # Compare fields independently of declaration order.
        actual = dict(
            field.split("=", 1) for field in result.split("(", 1)[1][:-1].split(", ")
        )
        assert actual == expected


def test_raw_color_repr():
    value = rev.ColorSensorV3.RawColor(1, 20, 300, 4000)
    assert repr(value) == "ColorSensorV3.RawColor(red=1, green=20, blue=300, ir=4000)"
    value.green = 42
    assert repr(value) == "ColorSensorV3.RawColor(red=1, green=42, blue=300, ir=4000)"


def test_periodic_status_repr_with_enum_and_boolean():
    value = rev.SparkLowLevel.PeriodicStatus8()
    value.setpoint = -1.25
    value.is_at_setpoint = True
    value.selected_pid_slot = rev.ClosedLoopSlot.SLOT2
    value.timestamp = 1234567890123
    assert repr(value) == (
        "SparkLowLevel.PeriodicStatus8(setpoint=-1.25, is_at_setpoint=True, "
        "selected_pid_slot=<ClosedLoopSlot.SLOT2: 2>, timestamp=1234567890123)"
    )


def signal_value(name):
    scalar_values = {
        "double": -1.25,
        "bool": True,
        "int": -42,
        "ClosedLoopSlot": rev.ClosedLoopSlot.SLOT2,
        "A301GearboxRPM": list(rev.A301.GearboxRPM.__members__.values())[-1],
    }
    if name in scalar_values:
        return scalar_values[name]
    for prefix, device, low_level in (
        ("Spark", rev.SparkBase, rev.SparkLowLevel),
        ("Detached", rev.DetachedEncoder, rev.DetachedEncoderLowLevel),
        ("ServoHub", rev.ServoHub, rev.ServoHubLowLevel),
        ("A301", rev.A301, rev.A301),
    ):
        if name.startswith(prefix):
            suffix = name[len(prefix) :]
            parent = low_level if suffix.startswith("PeriodicStatus") else device
            return getattr(parent, suffix)()
    raise AssertionError(f"Unhandled Signal specialization: {name}")


@pytest.mark.parametrize(
    "name", [name for name in dir(rev) if name.startswith("Signal_")]
)
@pytest.mark.parametrize("error", [rev.REVLibError.OK, rev.REVLibError.TIMEOUT])
def test_signal_repr_includes_value_error_and_timestamp(name, error):
    value = signal_value(name.removeprefix("Signal_"))
    signal = getattr(rev, name)(value, error, 1234567890123)
    assert repr(signal) == (
        f"{name}(value={value!r}, error={error!r}, timestamp=1234567890123)"
    )


def test_invalid_signal_repr_preserves_stored_value():
    signal = rev.Signal_double(-1.25, rev.REVLibError.TIMEOUT, 0)
    assert repr(signal) == (
        "Signal_double(value=-1.25, error=<REVLibError.TIMEOUT: 2>, timestamp=0)"
    )
