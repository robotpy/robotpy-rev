#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev
import wpilib


class Robot(wpilib.TimedRobot):
    def robot_init(self):
        # Create motor
        self.motor = rev.SparkMax(0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS)

        self.joystick = wpilib.Joystick(0)

        # Configuration parameters are set by calling the appropriate method on
        # a SparkMaxConfig object, then applying that configuration to the SPARK.
        self.config = rev.SparkMaxConfig()
        self.config.set_idle_mode(rev.SparkBaseConfig.IdleMode.COAST)
        self.config.open_loop_ramp_rate(0)

        if (
            self.motor.configure(
                self.config,
                rev.ResetMode.RESET_SAFE_PARAMETERS,
                rev.PersistMode.NO_PERSIST_PARAMETERS,
            )
            != rev.REVLibError.OK
        ):
            wpilib.SmartDashboard.put_string("Config", "Error")

        # Configuration accessors retrieve values currently stored on the
        # controller.
        if (
            self.motor.config_accessor.get_idle_mode()
            == rev.SparkBaseConfig.IdleMode.COAST
        ):
            wpilib.SmartDashboard.put_string("Idle Mode", "Coast")
        else:
            wpilib.SmartDashboard.put_string("Idle Mode", "Brake")

        wpilib.SmartDashboard.put_string(
            "Ramp Rate", str(self.motor.config_accessor.get_open_loop_ramp_rate())
        )

    def teleop_periodic(self):
        # Pair motor and the joystick's Y Axis
        self.motor.set(self.joystick.get_y())

        # Put Voltage, Temperature, and Motor Output onto SmartDashboard
        wpilib.SmartDashboard.put_number("Voltage", self.motor.get_bus_voltage())
        wpilib.SmartDashboard.put_number(
            "Temperature", self.motor.get_motor_temperature()
        )
        wpilib.SmartDashboard.put_number("Output", self.motor.get_applied_output())


if __name__ == "__main__":
    wpilib.run(Robot)
