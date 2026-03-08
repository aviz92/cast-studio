"""cast-run — execute run_demo.sh with a user-supplied demo.cfg."""

import subprocess
from pathlib import Path

from python_base_command import BaseCommand, CommandError

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


class Command(BaseCommand):
    help = "Run the demo engine (run_demo.sh) with your demo.cfg"
    version = "0.1.0"

    def add_arguments(self, parser):
        parser.add_argument(
            "cfg",
            nargs="?",
            default="demo/demo.cfg",
            help="Path to demo.cfg (default: demo/demo.cfg)",
        )

    def handle(self, **kwargs):
        cfg = Path(kwargs["cfg"])
        run_demo = TEMPLATES_DIR / "run_demo.sh"

        if not run_demo.exists():
            raise CommandError(f"run_demo.sh not found in package: {run_demo}")

        if not cfg.exists():
            raise CommandError(
                f"Config file not found: {cfg}\n"
                f"  Run: cast-init --dest {cfg.parent}"
            )

        self.logger.step(f"Running demo engine with config: {cfg}")
        result = subprocess.run(["bash", str(run_demo), str(cfg)])

        if result.returncode != 0:
            raise CommandError(f"run_demo.sh exited with code {result.returncode}")
