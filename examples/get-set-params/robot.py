# ----------------------------------------------------------------------------
# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.
# ----------------------------------------------------------------------------

import rev
import wpilib


class Robot(wpilib.TimedRobot):
    def robotInit(self):
        # Create motor
        self.motor = rev.CANSparkMax(1, rev.MotorType.kBrushless)

        self.joystick = wpilib.Joystick(0)

        # The restoreFactoryDefaults method can be used to reset the
        # configuration parameters in the SPARK MAX to their factory default
        # state. If no argument is passed, these parameters will not persist
        # between power cycles
        self.motor.restoreFactoryDefaults()

        # Parameters can be set by calling the appropriate set() method on the
        # CANSparkMax object whose properties you want to change
        #
        # Set methods will return one of three CANError values which will let
        # you know if the parameter was successfully set:
        #   CANError.kOk
        #   CANError.kError
        #   CANError.kTimeout
        if self.motor.setIdleMode(rev.IdleMode.kCoast) is not rev.CANError.kOk:
            wpilib.SmartDashboard.putString("Idle Mode", "Error")

        # Similarly, parameters will have a get() method which allows you to
        # retrieve their values from the controller
        if self.motor.getIdleMode() is rev.IdleMode.kCoast:
            wpilib.SmartDashboard.putString("Idle Mode", "Coast")
        else:
            wpilib.SmartDashboard.putString("Idle Mode", "Brake")

        # Set ramp rate to 0
        if self.motor.setOpenLoopRampRate(0) is not rev.CANError.kOk:
            wpilib.SmartDashboard.putString("Ramp Rate", "Error")

        # Read back ramp value
        wpilib.SmartDashboard.putString(
            "Ramp Rate", str(self.motor.getOpenLoopRampRate())
        )

    def teleopPeriodic(self):
        # Pair motor and the joystick's Y Axis
        self.motor.set(self.joystick.getY())

        # Put Voltage, Temperature, and Motor Output onto SmartDashboard
        wpilib.SmartDashboard.putNumber("Voltage", self.motor.getBusVoltage())
        wpilib.SmartDashboard.putNumber("Temperature", self.motor.getMotorTemperature())
        wpilib.SmartDashboard.putNumber("Output", self.motor.getAppliedOutput())


if __name__ == "__main__":
    wpilib.run(Robot)
