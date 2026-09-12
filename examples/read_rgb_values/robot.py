#!/usr/bin/env python3
#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import telemetry
import wpilib
from rev import ColorSensorV3


class MyRobot(wpilib.TimedRobot):
    """
    This is a simple example to show the values that can be read from the REV
    Color Sensor V3
    """

    def __init__(self):
        super().__init__()
        self.color_sensor = ColorSensorV3(wpilib.I2C.Port.PORT_0)

    def robot_periodic(self):
        # The method get_color() returns a normalized color value from the sensor and can be
        # useful if outputting the color to an RGB LED or similar. To
        # read the raw color, use get_raw_color().

        # The color sensor works best when within a few inches from an object in
        # well lit conditions (the built in LED is a big help here!). The farther
        # an object is the more light from the surroundings will bleed into the
        # measurements and make it difficult to accurately determine its color.
        detected_color = self.color_sensor.get_color()

        # The sensor returns a raw IR value of the infrared light detected.
        ir = self.color_sensor.get_ir()

        # Open the Telemetry table in your dashboard to see the detected color.
        telemetry.log("Red", detected_color.red)
        telemetry.log("Green", detected_color.green)
        telemetry.log("Blue", detected_color.blue)
        telemetry.log("IR", ir)

        # In addition to RGB IR values, the color sensor can also return an
        # infrared proximity value. The chip contains an IR led which will emit
        # IR pulses and measure the intensity of the return. When an object is
        # close the value of the proximity will be large (max 2047 with default
        # settings) and will approach zero when the object is far away.
        #
        # Proximity can be used to roughly approximate the distance of an object
        # or provide a threshold for when an object is close enough to provide
        # accurate color values.
        proximity = self.color_sensor.get_proximity()

        telemetry.log("Proximity", proximity)

        # `self.color_sensor.get_color()` returns a Color that is normalized.
        # The R, G, B values are scaled so that they add up to 1.
        # (`red + green + blue = 1`).
        # `.get_raw_color()` will return color data that is easier to
        # visualize but may be harder to use effectively in your code.

        raw_detected_color = self.color_sensor.get_raw_color()

        telemetry.log("Raw Red", raw_detected_color.red)
        telemetry.log("Raw Green", raw_detected_color.green)
        telemetry.log("Raw Blue", raw_detected_color.blue)
        telemetry.log("Raw IR", raw_detected_color.ir)


if __name__ == "__main__":
    wpilib.run(MyRobot)
