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


def test_motor_parameter_telemetry(robot, control):
    nt = ntcore.NetworkTableInstance.get_default()
    motor_sim = rev.SparkMaxSim(robot.motor, DCMotor.neo(1))
    motor_sim.set_bus_voltage(10.0)
    joystick = JoystickSim(robot.joystick)
    joystick.set_axes_available(2)
    joystick.set_y(0.5)

    with control.run_robot():
        control.step_timing(seconds=0.2, autonomous=False, enabled=True)
        assert nt.get_entry("/Telemetry/Idle Mode").get_string("") in ("Coast", "Brake")
        assert nt.get_entry("/Telemetry/Ramp Rate").get_string("") != ""
        assert nt.get_entry("/Telemetry/Voltage").get_double(-1) == 10.0
        # Preserve duty-cycle control regardless of the simulated battery voltage.
        assert motor_sim.get_setpoint() == 0.5
        assert (
            robot.motor.get_closed_loop_controller().get_control_type()
            == rev.SparkBase.ControlType.DUTY_CYCLE
        )
        for key in ("Voltage", "Temperature", "Output"):
            # Signal objects must be unwrapped to log numeric values, not strings.
            assert nt.get_topic(f"/Telemetry/{key}").get_type_string() == "double"
