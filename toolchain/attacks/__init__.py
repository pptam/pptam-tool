"""
Attack implementations live in this package.

Each attack can be provided either as:
- A class named `Attack` with constructor
    Attack(configuration, design_path, output_path, test_identifier)
  and a method:
    run(duration_seconds, stop_event)

or as a function:
    run(duration_seconds, stop_event, configuration, design_path, output_path, test_identifier)

The perform_attack plugin dynamically loads the module named by ATTACK_NAME
from configuration and invokes it during the test window.
"""

