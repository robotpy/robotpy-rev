#!/usr/bin/env python3

# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.

import wpilib
from rev import ColorSensorV3


class MyRobot(wpilib.TimedRobot):
    """
    This is a simple example to show the values that can be read from the REV
    Color Sensor V3
    """

    def robotInit(self):
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)

    def robotPeriodic(self):

        # The method getColor() returns a normalized color value from the sensor and can be
        # useful if outputting the color to an RGB LED or similar. To
        # read the raw color, use getRawColor().

        # The color sensor works best when within a few inches from an object in
        # well lit conditions (the built in LED is a big help here!). The farther
        # an object is the more light from the surroundings will bleed into the
        # measurements and make it difficult to accurately determine its color.
        detectedColor = self.colorSensor.getColor()

        # The sensor returns a raw IR value of the infrared light detected.
        ir = self.colorSensor.getIR()

        # Open Smart Dashboard or Shuffleboard to see the color detected by the
        # sensor.
        wpilib.SmartDashboard.putNumber("Red", detectedColor.red)
        wpilib.SmartDashboard.putNumber("Green", detectedColor.green)
        wpilib.SmartDashboard.putNumber("Blue", detectedColor.blue)
        wpilib.SmartDashboard.putNumber("IR", ir)

        # In addition to RGB IR values, the color sensor can also return an
        # infrared proximity value. The chip contains an IR led which will emit
        # IR pulses and measure the intensity of the return. When an object is
        # close the value of the proximity will be large (max 2047 with default
        # settings) and will approach zero when the object is far away.
        #
        # Proximity can be used to roughly approximate the distance of an object
        # or provide a threshold for when an object is close enough to provide
        # accurate color values.
        proximity = self.colorSensor.getProximity()

        wpilib.SmartDashboard.putNumber("Proximity", proximity)

        # `self.colorSensor.getColor()` returns a Color that is normalized.
        # The R, G, B values are scaled so that they add up to 1.
        # (`red + green + blue = 1`).
        # `.getRawColor()` will return color data that is easier to
        # visualize but may be harder to use effectively in your code.

        rawDetectedColor = self.colorSensor.getRawColor()

        wpilib.SmartDashboard.putNumber("Raw Red", rawDetectedColor.red)
        wpilib.SmartDashboard.putNumber("Raw Green", rawDetectedColor.green)
        wpilib.SmartDashboard.putNumber("Raw Blue", rawDetectedColor.blue)
        wpilib.SmartDashboard.putNumber("Raw IR", rawDetectedColor.ir)


if __name__ == "__main__":
    wpilib.run(MyRobot)
