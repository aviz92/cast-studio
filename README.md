![PyPI version](https://img.shields.io/pypi/v/cast-studio)
![Python](https://img.shields.io/badge/python->=3.9-blue)
![Development Status](https://img.shields.io/badge/status-alpha-orange)
![Maintenance](https://img.shields.io/maintenance/yes/2026)
![PyPI](https://img.shields.io/pypi/dm/cast-studio)
![License](https://img.shields.io/pypi/l/cast-studio)

---

# 🎬 cast-studio

Convert [asciinema](https://asciinema.org/) `.cast` recordings into **GIF** and **MP4** — and scaffold a generic demo-recording engine for any Python project.

---

## 📦 Installation

```bash
uv add cast-studio
```

> **System requirement:** `ffmpeg` must be installed.
> ```bash
> brew install ffmpeg        # macOS
> apt-get install ffmpeg     # Ubuntu / Debian
> ```

---

## 🚀 Features

- ✅ **cast → GIF** — High-quality 256-colour GIF via ffmpeg palette pass
- ✅ **cast → MP4** — H.264/x264 CRF-18 MP4 ready for GitHub Releases
- ✅ **Catppuccin Mocha theme** — Beautiful dark terminal rendering with Pillow
- ✅ **Generic demo engine** — `cast-run` + `demo.cfg` for any project
- ✅ **Any shell command** — Record pytest runs, scripts, CLIs — not just pytest
- ✅ **Multi-line descriptions** — Pipe-separated description lines per run
- ✅ **`python-base-command` CLI** — Structured, loggable CLI with `cast` / `cast-render` / `cast-init`

---

## ⚙️ Configuration

No `.env` needed. All config lives in `demo.cfg`:

```bash
PROJECT="my-library"
SUBTITLE="A short description"
INSTALL_CMD="pip install my-library"
REPO_URL="github.com/you/my-library"
PYPI_URL="pypi.org/project/my-library"

PYTEST=".venv/bin/pytest"
TESTS="tests/"

PAUSE_INTRO=2       # seconds after intro screen
PAUSE_BETWEEN=2     # seconds between runs
PAUSE_OUTRO=3       # seconds on outro screen

define_runs() {
  add_run "RUN 1 — feature A" "Short description." "$PYTEST $TESTS --flag"
  add_run "RUN 2 — script"   "Another feature."    "python scripts/my_script.py"
}
```

> `add_run "Title" "Line 1|Line 2" "any shell command"` — use `|` for multi-line descriptions.

---

## 🛠️ How to Use

1. **Install** — `uv add cast-studio` (and `brew install ffmpeg asciinema`)
3. **Create .cfg** — customise `demo.cfg` with your project's runs
4. **Record** — `asciinema rec -c "cast-run demo/demo.cfg" demo.cast`
5. **Render** — `cast-render demo.cast assets/demo --gif-only --title "my demo"` → `assets/demo.gif`
6. **Embed** — add `![demo](assets/demo.gif)` to your README

---

## 🚀 Quick Start

```bash
# 1. Install
uv add cast-studio
brew install ffmpeg asciinema   # macOS

# 2. Create demo/demo.cfg — set PROJECT, SUBTITLE, INSTALL_CMD, define_runs()
```

`demo/demo.cfg` structure:
```bash
PROJECT="my-library"
SUBTITLE="A short description"
INSTALL_CMD="uv add my-library"
REPO_URL="github.com/you/my-library"
PYPI_URL="pypi.org/project/my-library"

define_runs() {
  add_run "RUN 1 — feature A" "Short description." "pytest tests/ --flag"
  add_run "RUN 2 — script"   "Another feature."    "python scripts/my_script.py"
}
```

```bash
# 3. Record
asciinema rec -c "bash cast-run demo/demo.cfg" assets/demo/demo.cast

# 4. Render to GIF and MP4
cast-render assets/demo/demo.cast assets/demo/demo --gif-only --title "my-library demo"  # -> `assets/demo/demo.gif`
cast-render assets/demo/demo.cast assets/demo/demo --mp4-only --title "my-library demo"  # -> `assets/demo/demo.mp4`

# 5. Embed in README
# ![demo](assets/demo.gif)
```

---

## CLI Reference

### `cast-render`

| Flag | Default | Description |
|------|---------|-------------|
| `cast_file` | — | Path to `.cast` file |
| `output_base` | — | Output path without extension |
| `--title` | `""` | Title bar text |
| `--gif-only` | — | Produce GIF only |
| `--mp4-only` | — | Produce MP4 only |
| `--render-fps` | `30` | Internal PNG frame rate |
| `--gif-fps` | `10` | GIF output FPS |
| `--mp4-fps` | `30` | MP4 output FPS |
| `--hold` | `3.0` | Seconds to hold last frame |
| `--keep-frames` | — | Keep temporary PNG frames |

### `cast-init`

| Flag | Default | Description |
|------|---------|-------------|
| `--dest` | `scripts/record_demo` | Directory to scaffold into |
| `--force` | — | Overwrite existing files |

---

## 🤝 Contributing

If you have a helpful pattern or improvement to suggest:
Fork the repo
Create a new branch
Submit a pull request
I welcome additions that promote clean, productive, and maintainable development.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Thanks

Thanks for exploring this repository! <br>
Happy coding!

[![GitHub](https://img.shields.io/badge/GitHub-aviz92-181717?logo=github)](https://github.com/aviz92)
&nbsp; [![PyPI](https://img.shields.io/badge/PyPI-aviz-3775A9?logo=pypi)](https://pypi.org/user/aviz/)
&nbsp; [![Blog](https://img.shields.io/badge/Blog-aviz92.github.io-0066CC?logo=googlechrome)](https://aviz92.github.io/)
&nbsp; [![LinkedIn](https://img.shields.io/badge/LinkedIn-avi--zaguri-0A66C2?logo=linkedin)](https://www.linkedin.com/in/avi-zaguri-41869b11b)
