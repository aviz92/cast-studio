import shutil
from pathlib import Path

from python_base_command import BaseCommand, CommandError

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


class Command(BaseCommand):
    help = "Scaffold cast-studio demo scripts into your project"
    version = "0.1.0"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dest",
            default="scripts/record_demo",
            help="Destination directory (default: scripts/record_demo)",
        )
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing files",
        )

    def handle(self, **kwargs):
        dest = Path(kwargs["dest"])
        dest.mkdir(parents=True, exist_ok=True)

        files = {
            TEMPLATES_DIR / "run_demo.sh":      dest / "run_demo.sh",
            TEMPLATES_DIR / "demo.cfg.example": dest / "demo.cfg",
        }

        created = []
        skipped = []

        for src, dst in files.items():
            if not src.exists():
                raise CommandError(f"Template not found: {src}")
            if dst.exists() and not kwargs["force"]:
                skipped.append(str(dst))
                continue
            shutil.copy(src, dst)
            dst.chmod(dst.stat().st_mode | 0o755)
            created.append(str(dst))

        if created:
            self.logger.info("Created:")
            for f in created:
                self.logger.info(f"  {f}")

        if skipped:
            self.logger.warning("Already exists (use --force to overwrite):")
            for f in skipped:
                self.logger.warning(f"  {f}")

        if not created and not skipped:
            raise CommandError("No template files found.")

        self.logger.step(f"Next steps:")
        self.logger.info(f"  1. Edit  {dest}/demo.cfg")
        self.logger.info(f"  2. Record:")
        self.logger.info(f"       asciinema rec -c \"bash {dest}/run_demo.sh {dest}/demo.cfg\" demo.cast")
        self.logger.info(f"  3. Render:")
        self.logger.info(f"       cast-render demo.cast assets/demo")
