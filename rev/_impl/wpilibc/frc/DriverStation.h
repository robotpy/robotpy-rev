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

};

}  // namespace frc
