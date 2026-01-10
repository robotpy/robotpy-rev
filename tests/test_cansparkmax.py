import rev
from rev import REVLibError


def test_setfeedbackdevice():
    s = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
    e = s.getEncoder()
    p = s.getClosedLoopController()
    # assert p.setFeedbackDevice(e) == REVLibError.kOk


def test_get_fwd_limit():
    sm = rev.SparkMax(2, rev.SparkLowLevel.MotorType.kBrushless)
    switch = sm.getForwardLimitSwitch()
    switch.get()


def test_current_limit():
    sm = rev.SparkMax(1, rev.SparkLowLevel.MotorType.kBrushless)
    cfg = rev.SparkMaxConfig()
    cfg.secondaryCurrentLimit(50)
    sm.configure(
        cfg,
        rev.ResetMode.kResetSafeParameters,
        rev.PersistMode.kPersistParameters,
    )

    # assert hal_data["CAN"]["sparkmax-1"]["currentChop"] == 50.0
    # assert isinstance(hal_data["CAN"]["sparkmax-1"]["currentChop"], float)
    # assert hal_data["CAN"]["sparkmax-1"]["currentChopCycles"] == 0

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
    sm = rev.SparkMax(0, rev.SparkLowLevel.MotorType.kBrushless)
    pid = sm.getClosedLoopController()
    # pid.setOutputRange(-1, 1)
    # pid.setP(0.005)
    pid.setReference(5, rev.SparkBase.ControlType.kPosition)
