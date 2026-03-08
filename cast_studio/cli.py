"""
cast — main entry point, auto-discovers all commands.

Usage:
    cast render demo.cast assets/demo
    cast init
    cast --help
"""

from pathlib import Path

from python_base_command import Runner


def main():
    Runner(commands_dir=str(Path(__file__).parent / "commands")).run()


if __name__ == "__main__":
    main()
