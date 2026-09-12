#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import wpilib
from rev import ColorSensorV3, ColorMatch


class MyRobot(wpilib.TimedRobot):
    """
    This is a simple example to show the values that can be read from the REV
    Color Sensor V3
    """

    def robot_init(self):
        self.color_sensor = ColorSensorV3(wpilib.I2C.Port.PORT_0)

        # A Rev Color Match object is used to register and detect known colors. This can
        # be calibrated ahead of time or during operation.
        #
        # This object uses a simple euclidian distance to estimate the closest match
        # with given confidence range.
        self.color_matcher = ColorMatch()

        # Note: Any example colors should be calibrated as the user needs, these
        # are here as a basic example.
        self.blue_target = wpilib.Color(0.143, 0.427, 0.429)
        self.green_target = wpilib.Color(0.197, 0.561, 0.240)
        self.red_target = wpilib.Color(0.561, 0.232, 0.114)
        self.yellow_target = wpilib.Color(0.361, 0.524, 0.113)

        self.color_matcher.add_color_match(self.blue_target)
        self.color_matcher.add_color_match(self.green_target)
        self.color_matcher.add_color_match(self.red_target)
        self.color_matcher.add_color_match(self.yellow_target)

    def robot_periodic(self):
        # The method get_color() returns a normalized color value from the sensor and can be
        # useful if outputting the color to an RGB LED or similar. To
        # read the raw color, use get_raw_color().

        # The color sensor works best when within a few inches from an object in
        # well lit conditions (the built in LED is a big help here!). The farther
        # an object is the more light from the surroundings will bleed into the
        # measurements and make it difficult to accurately determine its color.
        detected_color = self.color_sensor.get_color()

        # Run the color match algorithm on our detected color. The confidence
        # specifies how close detected_color has to be to one of your colors
        # for it to match.
        match, confidence = self.color_matcher.match_closest_color(detected_color)

        color_string = ""

        if match == self.blue_target:
            color_string = "Blue"
        elif match == self.red_target:
            color_string = "Red"
        elif match == self.green_target:
            color_string = "Green"
        elif match == self.yellow_target:
            color_string = "Yellow"
        else:  # match is black
            color_string = "Unknown"

        # Open Smart Dashboard or Shuffleboard to see the color detected by the
        # sensor.
        wpilib.SmartDashboard.put_number("Red", detected_color.red)
        wpilib.SmartDashboard.put_number("Green", detected_color.green)
        wpilib.SmartDashboard.put_number("Blue", detected_color.blue)
        wpilib.SmartDashboard.put_number("Confidence", confidence)
        wpilib.SmartDashboard.put_string("Detected Color", color_string)


if __name__ == "__main__":
    wpilib.run(MyRobot)
