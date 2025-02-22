#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import swerveutils


def test_stepTowardsCircular1():
    current = 0.6408134451373411
    stepsize = 0.3455804605358387
    target = 0.0  # stepping towards zero direction
    result = swerveutils.stepTowardsCircular(
        current=current, stepsize=stepsize, target=target
    )
    # stepping towards zero angle should result in smaller absolute value
    assert abs(result) < abs(current)
