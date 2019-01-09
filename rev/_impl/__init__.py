import hal


if hal.isSimulation():

    import enum

    class MotorType(enum.IntEnum):
        kBrushed = 0
        kBrushless = 1

    class CANError(enum.IntEnum):
        kOK = 0
        kError = 1
        kTimeout = 2

    class CANSparkMax:
        def __init__(self, value, type):
            pass

        def set(self, value):
            raise NotImplementedError

        def get(self):
            raise NotImplementedError


else:
    from .rev_roborio import CANSparkMax, MotorType, CANError
