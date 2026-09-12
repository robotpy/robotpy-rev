#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import rev
import telemetry
import wpilib


class Robot(wpilib.TimedRobot):
    def __init__(self):
        super().__init__()
        # Create motor
        self.motor = rev.SparkMax(
            wpilib.CANPort.CAN_S0, 1, rev.SparkLowLevel.MotorType.BRUSHLESS
        )

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
            telemetry.log("Config", "Error")

        # Configuration accessors retrieve values currently stored on the
        # controller.
        if (
            self.motor.config_accessor.get_idle_mode()
            == rev.SparkBaseConfig.IdleMode.COAST
        ):
            telemetry.log("Idle Mode", "Coast")
        else:
            telemetry.log("Idle Mode", "Brake")

        telemetry.log(
            "Ramp Rate", str(self.motor.config_accessor.get_open_loop_ramp_rate())
        )

    def teleop_periodic(self):
        # Pair motor and the joystick's Y Axis
        self.motor.set_throttle(self.joystick.get_y())

        # Log Voltage, Temperature, and Motor Output to the Telemetry table.
        telemetry.log("Voltage", self.motor.get_bus_voltage().get())
        telemetry.log("Temperature", self.motor.get_motor_temperature().get())
        telemetry.log("Output", self.motor.get_applied_output().get())


if __name__ == "__main__":
    wpilib.run(Robot)
