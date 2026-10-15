#
# Copyright (c) FIRST and other WPILib contributors.
# Open Source Software; you can modify and/or share it under the terms of
# the WPILib BSD license file in the root directory of this project.
#

import math

import pytest
import rev
from wpilib.simulation import OnboardIMUSim, XboxControllerSim
from wpilib.testing.robot_tests import *
from wpimath import DCMotor, Rotation2d, SwerveModuleVelocity

from constants import ModuleConstants, NeoMotorConstants


def _modules(drive):
    return (drive.front_left, drive.front_right, drive.rear_left, drive.rear_right)


def test_get_heading_interprets_onboard_imu_yaw_as_radians(robot):
    drive = robot.robot_container.robot_drive
    OnboardIMUSim().set_yaw(math.pi / 2)

    assert drive.get_heading() == pytest.approx(90)


def test_drive_feedforward_is_nominal_voltage_over_free_speed(robot):
    # REVLib reads kV in volts per unit of velocity, so the feed forward must be
    # 12 V divided by the free speed (here in the SPARK's native RPM), not
    # 1 / free speed.
    for module in _modules(robot.robot_container.robot_drive):
        closed_loop = module.driving_spark.config_accessor.closed_loop
        assert closed_loop.feed_forward.getk_v() == pytest.approx(
            12.0 / NeoMotorConstants.FREE_SPEED_RPM
        )
        assert closed_loop.feed_forward.getk_v() == pytest.approx(
            12.0
            / ModuleConstants.DRIVE_WHEEL_FREE_SPEED_RPS
            * ModuleConstants.DRIVING_ENCODER_VELOCITY_FACTOR
        )
        assert closed_loop.get_feedback_sensor() == rev.FeedbackSensor.PRIMARY_ENCODER


def test_turning_uses_inverted_absolute_encoder_with_wrapping(robot):
    for module in _modules(robot.robot_container.robot_drive):
        accessor = module.turning_spark.config_accessor
        assert accessor.absolute_encoder.get_inverted()
        assert accessor.closed_loop.get_feedback_sensor() == (
            rev.FeedbackSensor.ABSOLUTE_ENCODER
        )
        assert accessor.closed_loop.get_position_wrapping_enabled()


def test_set_desired_state_applies_offset_in_native_units(robot):
    module = robot.robot_container.robot_drive.front_left

    module.set_desired_state(SwerveModuleVelocity(2.0, Rotation2d(0)))

    # 2 m/s at the wheel, in motor RPM
    driving = module.driving_closed_loop_controller
    assert driving.get_control_type() == rev.SparkBase.ControlType.VELOCITY
    assert driving.get_setpoint().get() == pytest.approx(
        2.0 / ModuleConstants.DRIVING_ENCODER_VELOCITY_FACTOR, rel=1e-6
    )
    # Straight ahead for the chassis is -pi/2 for the front left module, in rotations
    turning = module.turning_closed_loop_controller
    assert turning.get_control_type() == rev.SparkBase.ControlType.POSITION
    assert turning.get_setpoint().get() == pytest.approx(-0.25)


def test_get_state_converts_native_units(robot):
    module = robot.robot_container.robot_drive.rear_right
    sim = rev.SparkMaxSim(module.turning_spark, DCMotor.neo550(1))
    sim.get_absolute_encoder_sim().set_position(0.75)

    # 0.75 rotations is 270 degrees, minus the module's pi/2 offset
    assert module.get_state().angle.degrees() == pytest.approx(180)
    assert module.get_position().angle.degrees() == pytest.approx(180)


def test_right_bumper_sets_x(robot, control):
    drive = robot.robot_container.robot_drive
    controller = XboxControllerSim(robot.robot_container.driver_controller)
    controller.set_buttons_maximum_index(26)

    with control.run_robot():
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)
        controller.set_right_bumper_button(True)
        controller.notify_new_data()
        control.step_timing(seconds=0.1, autonomous=False, enabled=True)

        expected_degrees = (45, -45, -45, 45)
        for module, degrees in zip(_modules(drive), expected_degrees):
            assert module.desired_state.angle.degrees() == pytest.approx(degrees)
            assert module.driving_closed_loop_controller.get_setpoint().get() == 0


def test_autonomous_follows_trajectory_then_stops(robot, control):
    drive = robot.robot_container.robot_drive

    with control.run_robot():
        control.step_timing(seconds=1.0, autonomous=True, enabled=True)
        assert robot.autonomous_command.is_scheduled()
        assert any(
            module.driving_closed_loop_controller.get_setpoint().get() != 0
            for module in _modules(drive)
        )

        # The trajectory takes about 4.1 seconds
        control.step_timing(seconds=4.0, autonomous=True, enabled=True)
        assert not robot.autonomous_command.is_scheduled()
        for module in _modules(drive):
            assert module.driving_closed_loop_controller.get_setpoint().get() == 0
