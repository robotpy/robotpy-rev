# from unittest.mock import patch

# import pytest


# @pytest.fixture(scope="function")
# def _module_patch(request):
#     """This patch forces hal to reload each time we do this"""

#     # .. this seems inefficient

#     m = patch.dict("sys.modules", {})
#     m.start()
#     try:
#         yield
#     finally:
#         m.stop()


# @pytest.fixture(scope="function")
# def hal(_module_patch):
#     """Simulated hal module"""
#     import hal

#     return hal


# @pytest.fixture(scope="function")
# def hal_data(hal):
#     """Simulation data for HAL"""
#     import hal_impl.functions
#     import hal_impl.data

#     hal_impl.functions.reset_hal()
#     return hal_impl.data.hal_data


# @pytest.fixture(scope="function")
# def rev(hal_data):
#     import rev

#     return rev
