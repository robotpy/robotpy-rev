from ._impl import CANSparkMax, MotorType, CANError

try:
    from .version import __version__
except ImportError:  # pragma: nocover
    __version__ = "master"
