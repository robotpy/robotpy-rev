import rev
from rev import REVLibError


def test_setfeedbackdevice():
    s = rev.CANSparkMax(1, rev.CANSparkLowLevel.MotorType.kBrushless)
    e = s.getEncoder()
    p = s.getPIDController()
    assert p.setFeedbackDevice(e) == REVLibError.kOk


def test_get_fwd_limit():
    sm = rev.CANSparkMax(2, rev.CANSparkLowLevel.MotorType.kBrushless)
    switch = sm.getForwardLimitSwitch(rev.SparkLimitSwitch.Type.kNormallyOpen)
    switch.get()


def test_current_limit():
    sm = rev.CANSparkMax(1, rev.CANSparkLowLevel.MotorType.kBrushless)

    sm.setSecondaryCurrentLimit(50)

    # assert hal_data["CAN"]["sparkmax-1"]["currentChop"] == 50.0
    # assert isinstance(hal_data["CAN"]["sparkmax-1"]["currentChop"], float)
    # assert hal_data["CAN"]["sparkmax-1"]["currentChopCycles"] == 0

    sm.setSecondaryCurrentLimit(52.5, 5)

    # assert hal_data["CAN"]["sparkmax-1"]["currentChop"] == 52.5
    # assert hal_data["CAN"]["sparkmax-1"]["currentChopCycles"] == 5


# def test_faults(rev, hal_data):
#     sm = rev.CANSparkMax(1, rev.MotorType.kBrushed)
#     rev_sw = sm.getReverseLimitSwitch(rev.LimitSwitchPolarity.kNormallyOpen)
#     hal_data["CAN"]["sparkmax-1"]["faults"][rev.FaultID.kHardLimitRev] = False
#     assert not rev_sw.get()


# def test_frame_period():
#     sm = rev.CANSparkMax(2, rev.CANSparkLowLevel.MotorType.kBrushed)
#     sm.setPeriodicFramePeriod(rev.CANSparkLowLevel.PeriodicFrame.kStatus2, 20)
#     assert (
#         hal_data["CAN"]["sparkmax-2"]["frame_period"][rev.PeriodicFrame.kStatus2] == 20
#     )


def test_pid_set():
    sm = rev.CANSparkMax(0, rev.CANSparkLowLevel.MotorType.kBrushless)
    pid = sm.getPIDController()
    pid.setOutputRange(-1, 1)
    pid.setP(0.005)
    pid.setReference(5, rev.CANSparkBase.ControlType.kPosition)
