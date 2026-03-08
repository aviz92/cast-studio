"""ANSI terminal emulator — parses escape codes into a cell buffer."""

import re

# ── Catppuccin Mocha palette ──────────────────────────────────────────────────
BG      = (30,  30,  46)
FG      = (205, 214, 244)
TOPBAR  = (24,  24,  37)
TITLE_C = (147, 153, 178)

ANSI_PALETTE = {
    0:  (69,  71,  90),
    1:  (243, 139, 168),
    2:  (166, 227, 161),
    3:  (249, 226, 175),
    4:  (137, 180, 250),
    5:  (203, 166, 247),
    6:  (137, 220, 235),
    7:  (205, 214, 244),
    8:  (88,  91,  112),
    9:  (243, 139, 168),
    10: (166, 227, 161),
    11: (249, 226, 175),
    12: (137, 180, 250),
    13: (203, 166, 247),
    14: (137, 220, 235),
    15: (255, 255, 255),
}

ANSI_RE = re.compile(r'\x1b(?:\[([0-9;]*)([A-Za-z])|(.))')


class Attr:
    __slots__ = ("fg", "bg", "bold", "dim")

    def __init__(self):
        self.fg = self.bg = None
        self.bold = self.dim = False

    def copy(self):
        a = Attr()
        a.fg, a.bg, a.bold, a.dim = self.fg, self.bg, self.bold, self.dim
        return a

    def reset(self):
        self.fg = self.bg = None
        self.bold = self.dim = False

    def fg_rgb(self):
        if self.fg is None:
            return FG
        return ANSI_PALETTE.get(self.fg + (8 if self.bold and self.fg < 8 else 0), FG)

    def bg_rgb(self):
        return BG if self.bg is None else ANSI_PALETTE.get(self.bg, BG)


class Terminal:
    def __init__(self, cols: int = 130, rows: int = 30):
        self.cols, self.rows = cols, rows
        self.cx = self.cy = 0
        self.attr = Attr()
        self._empty_row = lambda: [(' ', Attr()) for _ in range(cols)]
        self.buf = [self._empty_row() for _ in range(rows)]

    def _clear(self):
        self.buf = [self._empty_row() for _ in range(self.rows)]

    def _scroll_up(self):
        self.buf.pop(0)
        self.buf.append(self._empty_row())

    def _apply_sgr(self, params):
        if not params or params == ['']:
            self.attr.reset()
            return
        i = 0
        while i < len(params):
            p = int(params[i]) if params[i] else 0
            if   p == 0:              self.attr.reset()
            elif p == 1:              self.attr.bold = True
            elif p == 2:              self.attr.dim  = True
            elif p == 22:             self.attr.bold = self.attr.dim = False
            elif 30 <= p <= 37:       self.attr.fg = p - 30
            elif p == 39:             self.attr.fg = None
            elif 40 <= p <= 47:       self.attr.bg = p - 40
            elif p == 49:             self.attr.bg = None
            elif 90 <= p <= 97:       self.attr.fg = p - 90 + 8
            elif 100 <= p <= 107:     self.attr.bg = p - 100 + 8
            i += 1

    def write(self, text: str):
        pos, n = 0, len(text)
        while pos < n:
            ch = text[pos]
            if ch == '\r':
                self.cx = 0; pos += 1; continue
            if ch == '\n':
                self.cy += 1
                if self.cy >= self.rows:
                    self._scroll_up(); self.cy = self.rows - 1
                pos += 1; continue
            if ch == '\b':
                if self.cx > 0: self.cx -= 1
                pos += 1; continue
            if ch == '\x1b':
                m = ANSI_RE.match(text, pos)
                if m:
                    params_str, final = m.group(1), m.group(2)
                    if final:
                        params = params_str.split(';') if params_str else ['']
                        if final == 'm':
                            self._apply_sgr(params)
                        elif final == 'H':
                            self.cy = max(0, min((int(params[0]) - 1 if params[0] else 0), self.rows - 1))
                            self.cx = max(0, min((int(params[1]) - 1 if len(params) > 1 and params[1] else 0), self.cols - 1))
                        elif final == 'A': self.cy = max(0, self.cy - (int(params[0]) if params[0] else 1))
                        elif final == 'B': self.cy = min(self.rows - 1, self.cy + (int(params[0]) if params[0] else 1))
                        elif final == 'C': self.cx = min(self.cols - 1, self.cx + (int(params[0]) if params[0] else 1))
                        elif final == 'D': self.cx = max(0, self.cx - (int(params[0]) if params[0] else 1))
                        elif final == 'J':
                            if (int(params[0]) if params[0] else 0) in (2, 3):
                                self._clear(); self.cx = self.cy = 0
                        elif final == 'K':
                            p = int(params[0]) if params[0] else 0
                            if p == 0:
                                for x in range(self.cx, self.cols):
                                    self.buf[self.cy][x] = (' ', Attr())
                            elif p == 2:
                                self.buf[self.cy] = self._empty_row()
                    pos = m.end(); continue
                else:
                    pos += 1; continue
            if self.cy < self.rows and self.cx < self.cols:
                self.buf[self.cy][self.cx] = (ch, self.attr.copy())
            self.cx += 1
            if self.cx >= self.cols:
                self.cx = 0; self.cy += 1
                if self.cy >= self.rows:
                    self._scroll_up(); self.cy = self.rows - 1
            pos += 1
