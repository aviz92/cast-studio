"""Render cast frames to PNG, then encode to GIF + MP4 via ffmpeg."""

import json
import shutil
import subprocess
from pathlib import Path

from cast_studio.renderer import Renderer, COLS, ROWS
from cast_studio.terminal import Terminal


def load_cast(path: str) -> tuple[dict, list]:
    lines = Path(path).read_text().strip().splitlines()
    header = json.loads(lines[0])
    events = []
    for line in lines[1:]:
        try:
            events.append(json.loads(line))
        except Exception:
            pass
    return header, events


def render_frames(
    cast_file: str,
    frames_dir: Path,
    title: str = "",
    render_fps: int = 30,
    hold_secs: float = 3.0,
) -> int:
    print(f"\n[1/3] Rendering frames: {cast_file}")
    _, events = load_cast(cast_file)
    total_time = events[-1][0] if events else 1.0
    print(f"      {len(events)} events  |  {total_time:.2f}s  |  {render_fps}fps")

    renderer = Renderer(cols=COLS, rows=ROWS, title=title)
    print(f"      Frame size: {renderer.img_w}×{renderer.img_h}px")

    term = Terminal(COLS, ROWS)
    frames_dir.mkdir(parents=True, exist_ok=True)

    interval = 1.0 / render_fps
    sample_times = [i * interval for i in range(int(total_time / interval) + 2)]
    ei = n = 0

    for t in sample_times:
        while ei < len(events) and events[ei][0] <= t:
            _, kind, text = events[ei]
            if kind == "o":
                term.write(text)
            ei += 1
        renderer.render_frame(term).save(frames_dir / f"f{n:05d}.png")
        n += 1
        if n % 90 == 0:
            pct = int(100 * n / len(sample_times))
            print(f"      {pct}%  ({n}/{len(sample_times)} frames, t={t:.1f}s)")

    # Hold last frame
    last = frames_dir / f"f{n-1:05d}.png"
    for _ in range(int(hold_secs * render_fps)):
        shutil.copy(last, frames_dir / f"f{n:05d}.png")
        n += 1

    print(f"      Done — {n} frames saved")
    return n


def encode_gif(frames_dir: Path, out_gif: str, render_fps: int = 30, gif_fps: int = 10):
    print(f"\n[2/3] Encoding GIF → {out_gif}  ({gif_fps}fps)")
    palette = "/tmp/_cast_studio_palette.png"

    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(render_fps),
        "-i", str(frames_dir / "f%05d.png"),
        "-vf", f"fps={gif_fps},palettegen=max_colors=256:stats_mode=diff",
        palette,
    ], check=True, capture_output=True)

    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(render_fps),
        "-i", str(frames_dir / "f%05d.png"),
        "-i", palette,
        "-lavfi", f"fps={gif_fps}[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
        out_gif,
    ], check=True, capture_output=True)

    mb = Path(out_gif).stat().st_size / 1024 / 1024
    print(f"      {out_gif}  ({mb:.1f} MB)")


def encode_mp4(frames_dir: Path, out_mp4: str, render_fps: int = 30, mp4_fps: int = 30):
    print(f"\n[3/3] Encoding MP4 → {out_mp4}  ({mp4_fps}fps)")

    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(render_fps),
        "-i", str(frames_dir / "f%05d.png"),
        "-vf", f"fps={mp4_fps}",
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        out_mp4,
    ], check=True, capture_output=True)

    mb = Path(out_mp4).stat().st_size / 1024 / 1024
    print(f"      {out_mp4}  ({mb:.1f} MB)")
