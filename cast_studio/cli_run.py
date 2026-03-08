"""Entry point for `cast-run` — alias for the run command."""

import sys

from python_base_command import CommandRegistry

from cast_studio.commands.cast import Command


def main():
    registry = CommandRegistry()
    registry.register("run")(Command)
    sys.argv.insert(1, "run")
    registry.run()
