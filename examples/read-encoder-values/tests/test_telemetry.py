#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import ntcore
import rev
from wpilib.simulation import JoystickSim
from wpimath import DCMotor
from wpilib.testing.robot_tests import *


def test_encoder_telemetry(robot, control):
    nt = ntcore.NetworkTableInstance.get_default()
    motor_sim = rev.SparkMaxSim(robot.motor, DCMotor.neo(1))
    encoder_sim = motor_sim.get_relative_encoder_sim()
    encoder_sim.set_position(12.5)
    encoder_sim.set_velocity(123.5)
    joystick = JoystickSim(robot.joystick)
    joystick.set_axes_available(2)
    joystick.set_y(0.5)

    with control.run_robot():
        control.step_timing(seconds=0.2, autonomous=False, enabled=True)
        assert nt.get_entry("/Telemetry/Encoder Position").get_double(-1) == 12.5
        assert nt.get_entry("/Telemetry/Encoder Velocity").get_double(-1) == 123.5
        assert motor_sim.get_setpoint() == 0.5
        assert (
            robot.motor.get_closed_loop_controller().get_control_type()
            == rev.SparkBase.ControlType.DUTY_CYCLE
        )
