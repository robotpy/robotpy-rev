import math


def stepTowards(current: float, target: float, stepsize: float) -> float:
    """Steps a value towards a target with a specified step size.

    :param current:  The current or starting value.  Can be positive or negative.
    :param target:   The target value the algorithm will step towards.  Can be positive or negative.
    :param stepsize: The maximum step size that can be taken.

    :returns: The new value for {@code current} after performing the specified step towards the specified target.
    """

    if abs(current - target) <= stepsize:
        return target

    elif target < current:
        return current - stepsize

    else:
        return current + stepsize


def stepTowardsCircular(current: float, target: float, stepsize: float) -> float:
    """Steps a value (angle) towards a target (angle) taking the shortest path with a specified step size.

    :param current:  The current or starting angle (in radians).  Can lie outside the 0 to 2*PI range.
    :param target:   The target angle (in radians) the algorithm will step towards.  Can lie outside the 0 to 2*PI range.
    :param stepsize: The maximum step size that can be taken (in radians).

    :returns: The new angle (in radians) for {@code current} after performing the specified step towards the specified target.
              This value will always lie in the range 0 to 2*PI (exclusive).
    """

    current = wrapAngle(current)
    target = wrapAngle(target)

    stepDirection = math.copysign(target - current, 1)
    difference = abs(current - target)

    if difference <= stepsize:
        return target
    elif difference > math.pi:  # does the system need to wrap over eventually?
        # handle the special case where you can reach the target in one step while also wrapping
        if (
            current + math.tau - target < stepsize
            or target + math.tau - current < stepsize
        ):
            return target
        else:
            # this will handle wrapping gracefully
            return wrapAngle(current - stepDirection * stepsize)
    else:
        return current + stepDirection * stepsize


def angleDifference(angleA: float, angleB: float) -> float:
    """Finds the (unsigned) minimum difference between two angles including calculating across 0.

    :param angleA: An angle (in radians).
    :param angleB: An angle (in radians).

    :returns: The (unsigned) minimum difference between the two angles (in radians).
    """
    difference = abs(angleA - angleB)
    return math.tau - difference if difference > math.pi else difference


def wrapAngle(angle: float) -> float:
    """Wraps an angle until it lies within the range from 0 to 2*PI (exclusive).

    :param angle: The angle (in radians) to wrap.  Can be positive or negative and can lie multiple wraps outside the output range.

    :returns: An angle (in radians) from 0 and 2*PI (exclusive).
    """

    twoPi = math.tau

    # Handle this case separately to avoid floating point errors with the floor after the division in the case below
    if angle == twoPi:
        return 0.0
    elif angle > twoPi:
        return angle - twoPi * math.floor(angle / twoPi)
    elif angle < 0.0:
        return angle + twoPi * (math.floor((-angle) / twoPi) + 1)
    else:
        return angle
