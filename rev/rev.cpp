#include <semiwrap_init.rev._rev.hpp>

// rev doesn't expose the internal API, but you need to call these
// to initialize the library otherwise it crashes
extern "C" {
void *getRevLibWpiDriver(void);
void setREVLibDriver(void *newDriver);
}

SEMIWRAP_PYBIND11_MODULE(m) {
  setREVLibDriver(getRevLibWpiDriver());

  initWrapper(m);
}