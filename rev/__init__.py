from ._impl import (
    CANSparkMax,
    MotorType,
    CANError,
    LimitSwitch,
    LimitSwitchPolarity,
    ControlType,
    IdleMode,
)

try:
    from .version import __version__
except ImportError:  # pragma: nocover
    __version__ = "master"
