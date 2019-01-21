/*----------------------------------------------------------------------------*/
/* Copyright (c) 2008-2018 FIRST. All Rights Reserved.                        */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

#include "frc/DriverStation.h"

#include <hal/HAL.h>
#include <wpi/SmallString.h>
#include <wpi/StringRef.h>

using namespace frc;

DriverStation& DriverStation::GetInstance() {
  static DriverStation instance;
  return instance;
}

void DriverStation::ReportError(const wpi::Twine& error) {
  wpi::SmallString<128> temp;
  HAL_SendError(1, 1, 0, error.toNullTerminatedStringRef(temp).data(), "", "",
                1);
}

void DriverStation::ReportWarning(const wpi::Twine& error) {
  wpi::SmallString<128> temp;
  HAL_SendError(0, 1, 0, error.toNullTerminatedStringRef(temp).data(), "", "",
                1);
}

void DriverStation::ReportError(bool isError, int32_t code,
                                const wpi::Twine& error,
                                const wpi::Twine& location,
                                const wpi::Twine& stack) {
  wpi::SmallString<128> errorTemp;
  wpi::SmallString<128> locationTemp;
  wpi::SmallString<128> stackTemp;
  HAL_SendError(isError, code, 0,
                error.toNullTerminatedStringRef(errorTemp).data(),
                location.toNullTerminatedStringRef(locationTemp).data(),
                stack.toNullTerminatedStringRef(stackTemp).data(), 1);
}

double DriverStation::GetMatchTime() const {
  int32_t status;
  return HAL_GetMatchTime(&status);
}
