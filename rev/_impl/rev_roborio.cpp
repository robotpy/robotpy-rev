
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// Use this to release the gil
typedef py::call_guard<py::gil_scoped_release> release_gil;

// REV includes
#include "rev/CANSparkMax.h"

PYBIND11_MODULE(rev_roborio, m) {
    py::enum_<rev::CANSparkMax::MotorType>(m, "MotorType")
        .value("kBrushed", rev::CANSparkMax::MotorType::kBrushed)
        .value("kBrushless", rev::CANSparkMax::MotorType::kBrushless);

    py::enum_<rev::CANError>(m, "CANError")
        .value("kOK", rev::CANError::kOK)
        .value("kError", rev::CANError::kError)
        .value("kTimeout", rev::CANError::kTimeout);

    py::class_<rev::CANSparkMax> cls(m, "CANSparkMax");
    cls.def(py::init<int, rev::CANSparkMax::MotorType>(), release_gil())
       .def("set", &rev::CANSparkMax::Set, release_gil())
       .def("get", &rev::CANSparkMax::Get, release_gil());
}