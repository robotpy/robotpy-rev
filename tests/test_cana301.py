import rev


def test_set_velocity():
    a301 = rev.A301(0, 0)
    a301.setVelocity(12.34)


def test_set_relative_position():
    a301 = rev.A301(0, 0)
    a301.setRelativePositionWithSpeed(12.34, 350.0)
