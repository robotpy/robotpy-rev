import os
import subprocess
import sys

BASE_TESTS = [
    "can-arcade-drive",
    "can-tank-drive",
    "getting-started",
    "limit-switch",
]

IGNORED_TESTS = [
    "color_match",
    "get-set-params",
    "maxswerve",
    "position-pid-control",
    "read_rgb_values",
    "read-encoder-values",
    "smart-motion",
    "velocity-pid-control",
]  # Add ignored tests if any
EVERY_TESTS = BASE_TESTS + IGNORED_TESTS
TESTS = BASE_TESTS

script_dir = os.path.dirname(__file__)

robot_files = []
for root, dirs, files in os.walk("."):
    if "robot.py" in files:
        robot_files.append(os.path.relpath(root, "."))

for file in robot_files:
    print("found: " + file)
    if file not in EVERY_TESTS:
        if not os.getenv("FORCE_ANYWAYS"):
            print("ERROR: Not every robot.py file is in the list of tests!")
            exit(1)

for test in TESTS:
    print(f"Running test: {test}")
    os.chdir(os.path.join(script_dir, test))
    subprocess.run([sys.executable, "-m", "robotpy", "test", "--builtin"])
    os.chdir(script_dir)
