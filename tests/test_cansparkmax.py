import wpilib

import rev
from rev import REVLibError


def test_setfeedbackdevice():
    s = rev.SparkMax(wpilib.CANPort.CAN_S0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS)
    e = s.get_encoder()
    p = s.get_closed_loop_controller()
    # assert p.set_feedback_device(e) == REVLibError.OK


def test_get_fwd_limit():
    sm = rev.SparkMax(wpilib.CANPort.CAN_S0, 2, rev.SparkLowLevel.MotorType.BRUSHLESS)
    switch = sm.get_forward_limit_switch()
    switch.get()


def test_current_limit():
    sm = rev.SparkMax(wpilib.CANPort.CAN_S0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS)
    cfg = rev.SparkMaxConfig()
    cfg.secondary_current_limit(50)
    sm.configure(
        cfg,
        rev.ResetMode.RESET_SAFE_PARAMETERS,
        rev.PersistMode.PERSIST_PARAMETERS,
    )

    # assert hal_data["CAN"]["sparkmax-1"]["currentChop"] == 50.0
    # assert isinstance(hal_data["CAN"]["sparkmax-1"]["currentChop"], float)
    # assert hal_data["CAN"]["sparkmax-1"]["currentChopCycles"] == 0

    # assert hal_data["CAN"]["sparkmax-1"]["currentChop"] == 52.5
    # assert hal_data["CAN"]["sparkmax-1"]["currentChopCycles"] == 5


# def test_faults(rev, hal_data):
#     sm = rev.SparkMax(wpilib.CANPort.CAN_S0, 1, rev.SparkLowLevel.MotorType.BRUSHED)
#     rev_sw = sm.get_reverse_limit_switch()
#     hal_data["CAN"]["sparkmax-1"]["faults"][rev.FaultID.HARD_LIMIT_REV] = False
#     assert not rev_sw.get()


# def test_frame_period():
#     sm = rev.SparkMax(wpilib.CANPort.CAN_S0, 2, rev.SparkLowLevel.MotorType.BRUSHED)
#     sm.set_periodic_frame_period(rev.SparkLowLevel.PeriodicFrame.STATUS_2, 20)
#     assert (
#         hal_data["CAN"]["sparkmax-2"]["frame_period"][rev.PeriodicFrame.STATUS_2] == 20
#     )


def test_pid_set():
    sm = rev.SparkMax(wpilib.CANPort.CAN_S0, 0, rev.SparkLowLevel.MotorType.BRUSHLESS)
    pid = sm.get_closed_loop_controller()
    # cfg = rev.SparkMaxConfig()
    # cfg.closed_loop.P(0.005).output_range(-1, 1)
    pid.set_setpoint(5, rev.SparkBase.ControlType.POSITION)
