"""Pillow-based terminal frame renderer."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from cast_studio.terminal import BG, TOPBAR, TITLE_C, Terminal

FONT_PATH      = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FONT_SIZE      = 13

COLS = 130
ROWS = 30


def _find_font(path: str) -> str:
    """Return path if it exists, else fall back to a PIL default."""
    return path if Path(path).exists() else None  # Pillow uses default if None


class Renderer:
    def __init__(self, cols: int = COLS, rows: int = ROWS, title: str = ""):
        self.cols, self.rows = cols, rows
        self.title = title

        reg_path  = _find_font(FONT_PATH)
        bold_path = _find_font(FONT_BOLD_PATH)
        self.font_reg  = ImageFont.truetype(reg_path,  FONT_SIZE) if reg_path  else ImageFont.load_default()
        self.font_bold = ImageFont.truetype(bold_path, FONT_SIZE) if bold_path else self.font_reg

        bbox = self.font_reg.getbbox("M")
        self.cw = bbox[2] - bbox[0]
        self.ch = bbox[3] - bbox[1] + 3
        self.pad_x   = 8
        self.pad_top = 28
        self.pad_bot = 6
        self.img_w = self.pad_x * 2 + cols * self.cw
        self.img_h = self.pad_top + rows * self.ch + self.pad_bot

    def render_frame(self, term: Terminal) -> Image.Image:
        img  = Image.new("RGB", (self.img_w, self.img_h), BG)
        draw = ImageDraw.Draw(img)

        # Top bar
        draw.rectangle([(0, 0), (self.img_w, self.pad_top - 1)], fill=TOPBAR)
        for xi, color in enumerate([(243, 139, 168), (249, 226, 175), (166, 227, 161)]):
            cx_ = 12 + xi * 18
            cy_ = self.pad_top // 2
            draw.ellipse([(cx_-5, cy_-5), (cx_+5, cy_+5)], fill=color)
        if self.title:
            tw = draw.textlength(self.title, font=self.font_reg)
            draw.text(((self.img_w - tw) / 2, 7), self.title, fill=TITLE_C, font=self.font_reg)

        # Terminal cells
        for row_idx, row in enumerate(term.buf):
            y = self.pad_top + row_idx * self.ch
            for col_idx, (ch, attr) in enumerate(row):
                x = self.pad_x + col_idx * self.cw
                if attr.bg_rgb() != BG:
                    draw.rectangle([(x, y), (x + self.cw - 1, y + self.ch - 1)], fill=attr.bg_rgb())
                if ch and ch != ' ':
                    font = self.font_bold if attr.bold else self.font_reg
                    draw.text((x, y), ch, fill=attr.fg_rgb(), font=font)

        return img
