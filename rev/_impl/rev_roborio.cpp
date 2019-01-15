
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// Use this to release the gil
typedef py::call_guard<py::gil_scoped_release> release_gil;

// REV includes
#include "rev/CANDigitalInput.h"
#include "rev/CANEncoder.h"
#include "rev/CANError.h"
#include "rev/CANPIDController.h"
#include "rev/CANSparkMax.h"
#include "rev/ControlType.h"

PYBIND11_MODULE(rev_roborio, m) {

    //#include "autogen/CANDigitalInput.cpp.inc"
    // #include "autogen/CANEncoder.cpp.inc"
    // #include "autogen/CANPIDController.cpp.inc"
     #include "autogen/CANSparkMax.cpp.inc"

    #include "autogen/rev_enums.cpp.inc"
}