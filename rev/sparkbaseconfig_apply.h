#pragma once

template <typename T, typename Cls>
void bind_sparkbaseconfig_apply(Cls &cls) {
    using namespace rev::spark;

    auto sparkBaseConfigType = py::type::of<SparkBaseConfig>();

    cls
        .def("apply", [=](T &self, SparkBaseConfig &config) -> T& {
            sparkBaseConfigType.attr("apply")(self, config);
            return self;
        }, py::arg("config"))
        .def("apply", [=](T &self, AbsoluteEncoderConfig &config) -> T& {
            sparkBaseConfigType.attr("apply")(self, config);
            return self;
        }, py::arg("config"))
        .def("apply", [=](T &self, AnalogSensorConfig &config) -> T& {
            sparkBaseConfigType.attr("apply")(self, config);
            return self;
        }, py::arg("config"))
        .def("apply", [=](T &self, EncoderConfig &config) -> T& {
            sparkBaseConfigType.attr("apply")(self, config);
            return self;
        }, py::arg("config"))
        .def("apply", [=](T &self, LimitSwitchConfig &config) -> T& {
            sparkBaseConfigType.attr("apply")(self, config);
            return self;
        }, py::arg("config"))
        .def("apply", [=](T &self, SoftLimitConfig &config) -> T& {
            sparkBaseConfigType.attr("apply")(self, config);
            return self;
        }, py::arg("config"))
        .def("apply", [=](T &self, ClosedLoopConfig &config) -> T& {
            sparkBaseConfigType.attr("apply")(self, config);
            return self;
        }, py::arg("config"))
        .def("apply", [=](T &self, SignalsConfig &config) -> T& {
            sparkBaseConfigType.attr("apply")(self, config);
            return self;
        }, py::arg("config"))
    ;
}