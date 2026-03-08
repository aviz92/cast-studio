"""
cast-init — convenience alias for `cast init`.

Usage:
    cast-init
    cast-init --dest scripts/demo --force
"""

import sys

from python_base_command import CommandRegistry

from cast_studio.commands.init import Command


def main():
    registry = CommandRegistry()
    registry.register("init")(Command)
    sys.argv.insert(1, "init")
    registry.run()


if __name__ == "__main__":
    main()
