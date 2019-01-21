/*----------------------------------------------------------------------------*/
/* Copyright (c) 2008-2018 FIRST. All Rights Reserved.                        */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

#pragma once

#include <wpi/Twine.h>

#include "frc/ErrorBase.h"

namespace frc {

/**
 * Provide access to the network communication data to / from the Driver
 * Station.
 */
class DriverStation : public ErrorBase {
 public:
  /**
   * Return a reference to the singleton DriverStation.
   *
   * @return Reference to the DS instance
   */
  static DriverStation& GetInstance();

  /**
   * Report an error to the DriverStation messages window.
   *
   * The error is also printed to the program console.
   */
  static void ReportError(const wpi::Twine& error);

  /**
   * Report a warning to the DriverStation messages window.
   *
   * The warning is also printed to the program console.
   */
  static void ReportWarning(const wpi::Twine& error);

  /**
   * Report an error to the DriverStation messages window.
   *
   * The error is also printed to the program console.
   */
  static void ReportError(bool isError, int code, const wpi::Twine& error,
                          const wpi::Twine& location, const wpi::Twine& stack);

  /**
   * Return the approximate match time.
   *
   * The FMS does not send an official match time to the robots, but does send
   * an approximate match time. The value will count down the time remaining in
   * the current period (auto or teleop).
   *
   * Warning: This is not an official time (so it cannot be used to dispute ref
   * calls or guarantee that a function will trigger before the match ends).
   *
   * The Practice Match function of the DS approximates the behaviour seen on
   * the field.
   *
   * @return Time remaining in current match period (auto or teleop)
   */
  double GetMatchTime() const;
};

}  // namespace frc
