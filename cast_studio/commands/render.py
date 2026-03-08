import shutil
from pathlib import Path

from python_base_command import BaseCommand, CommandError

from cast_studio.encoder import render_frames, encode_gif, encode_mp4


class Command(BaseCommand):
    help = "Convert an asciinema .cast file to GIF and/or MP4"
    version = "0.1.0"

    def add_arguments(self, parser):
        parser.add_argument(
            "cast_file",
            help="Path to the .cast input file",
        )
        parser.add_argument(
            "output_base",
            help="Output base path, e.g. assets/demo → demo.gif + demo.mp4",
        )
        parser.add_argument(
            "--title",
            default="",
            help="Window title bar text (default: empty)",
        )
        parser.add_argument(
            "--gif-only",
            action="store_true",
            help="Produce GIF only (skip MP4)",
        )
        parser.add_argument(
            "--mp4-only",
            action="store_true",
            help="Produce MP4 only (skip GIF)",
        )
        parser.add_argument(
            "--render-fps",
            type=int,
            default=30,
            metavar="N",
            help="Internal render FPS used for PNG frames (default: 30)",
        )
        parser.add_argument(
            "--gif-fps",
            type=int,
            default=10,
            metavar="N",
            help="GIF output FPS (default: 10)",
        )
        parser.add_argument(
            "--mp4-fps",
            type=int,
            default=30,
            metavar="N",
            help="MP4 output FPS (default: 30)",
        )
        parser.add_argument(
            "--hold",
            type=float,
            default=3.0,
            metavar="SEC",
            help="Seconds to hold the last frame (default: 3.0)",
        )
        parser.add_argument(
            "--keep-frames",
            action="store_true",
            help="Keep temporary PNG frames after encoding (useful for debugging)",
        )

    def handle(self, **kwargs):
        cast_file = kwargs["cast_file"]
        output_base = kwargs["output_base"]

        if not Path(cast_file).exists():
            raise CommandError(f"Cast file not found: {cast_file}")

        if kwargs["gif_only"] and kwargs["mp4_only"]:
            raise CommandError("Cannot use --gif-only and --mp4-only together.")

        Path(output_base).parent.mkdir(parents=True, exist_ok=True)

        do_gif = not kwargs["mp4_only"]
        do_mp4 = not kwargs["gif_only"]

        frames_dir = Path("/tmp/_cast_studio_frames")
        if frames_dir.exists():
            shutil.rmtree(frames_dir)

        self.logger.step("Rendering PNG frames...")
        render_frames(
            cast_file=cast_file,
            frames_dir=frames_dir,
            title=kwargs["title"],
            render_fps=kwargs["render_fps"],
            hold_secs=kwargs["hold"],
        )

        if do_gif:
            self.logger.step("Encoding GIF...")
            encode_gif(frames_dir, output_base + ".gif", kwargs["render_fps"], kwargs["gif_fps"])

        if do_mp4:
            self.logger.step("Encoding MP4...")
            encode_mp4(frames_dir, output_base + ".mp4", kwargs["render_fps"], kwargs["mp4_fps"])

        if not kwargs["keep_frames"]:
            shutil.rmtree(frames_dir)

        self.logger.info("Done.")
        if do_gif:
            self.logger.info(f"  GIF → {output_base}.gif")
        if do_mp4:
            self.logger.info(f"  MP4 → {output_base}.mp4")
