#!/usr/bin/env python3

# Copyright (c) 2017-2018 FIRST. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.

import wpilib
from rev import ColorSensorV3, ColorMatch


class MyRobot(wpilib.TimedRobot):
    """
    This is a simple example to show the values that can be read from the REV
    Color Sensor V3
    """

    def robotInit(self):
        self.colorSensor = ColorSensorV3(wpilib.I2C.Port.kOnboard)

        # A Rev Color Match object is used to register and detect known colors. This can
        # be calibrated ahead of time or during operation.
        #
        # This object uses a simple euclidian distance to estimate the closest match
        # with given confidence range.
        self.colorMatcher = ColorMatch()

        # Note: Any example colors should be calibrated as the user needs, these
        # are here as a basic example.
        self.blueTarget = wpilib.Color(0.143, 0.427, 0.429)
        self.greenTarget = wpilib.Color(0.197, 0.561, 0.240)
        self.redTarget = wpilib.Color(0.561, 0.232, 0.114)
        self.yellowTarget = wpilib.Color(0.361, 0.524, 0.113)

        colorMatcher.addColorMatch(blueTarget)
        colorMatcher.addColorMatch(greenTarget)
        colorMatcher.addColorMatch(redTarget)
        colorMatcher.addColorMatch(yellowTarget)

    def robotPeriodic(self):

        # The method GetColor() returns a normalized color value from the sensor and can be
        # useful if outputting the color to an RGB LED or similar. To
        # read the raw color, use GetRawColor().

        # The color sensor works best when within a few inches from an object in
        # well lit conditions (the built in LED is a big help here!). The farther
        # an object is the more light from the surroundings will bleed into the
        # measurements and make it difficult to accurately determine its color.
        detectedColor = self.colorSensor.getColor()

        # Run the color match algorithm on our detected color. The confidence
        # specifies how close the detectedColor has to be to one of your colors
        # for it to match.
        confidence = 0.0
        match = self.colorMatcher.matchClosestColor(detectedColor, confidence)

        colorString = ""

        if match == self.blueTarget:
            colorString = "Blue"
        elif match == self.redTarget:
            colorString = "Red"
        elif match == self.greenTarget:
            colorString = "Green"
        elif match == self.yellowTarget:
            colorString = "Yellow"
        else:  # match is black
            colorString = "Unknown"

        # Open Smart Dashboard or Shuffleboard to see the color detected by the
        # sensor.
        wpilib.SmartDashboard.putNumber("Red", detectedColor.red)
        wpilib.SmartDashboard.putNumber("Green", detectedColor.green)
        wpilib.SmartDashboard.putNumber("Blue", detectedColor.blue)
        wpilib.SmartDashboard.putNumber("Confidence", confidence)
        wpilib.SmartDashboard.putString("Detected Color", colorString)


if __name__ == "__main__":
    wpilib.run(MyRobot)
