"""
cast-render — convenience alias for `cast render`.

Usage:
    cast-render demo.cast assets/demo
    cast-render demo.cast assets/demo --gif-only
"""

import sys

from python_base_command import CommandRegistry

from cast_studio.commands.render import Command


def main():
    registry = CommandRegistry()
    registry.register("render")(Command)
    sys.argv.insert(1, "render")
    registry.run()


if __name__ == "__main__":
    main()
