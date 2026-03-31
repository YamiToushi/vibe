import tkinter as tk
from tkinter import ttk
import random
import string
import math

UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS    = string.digits
SYMBOLS   = "!@#$%^&*()_+-=[]{}|;:,.<>?"

# ── Palette ───────────────────────────────────────────────────────────────────
BG        = "#1e1e2e"
SURFACE   = "#313244"
SURFACE2  = "#45475a"
TEXT      = "#cdd6f4"
SUBTEXT   = "#a6adc8"
MUTED     = "#6c7086"
BLUE      = "#89b4fa"
GREEN     = "#a6e3a1"
YELLOW    = "#f9e2af"
PEACH     = "#fab387"
RED       = "#f38ba8"
LAVENDER  = "#b4befe"


class PasswordGenerator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build_ui()

    # ──────────────────────────────────────────────────────────────── UI ──────

    def _build_ui(self):
        # ── Title ─────────────────────────────────────────────────────────────
        tk.Label(self, text="Password Generator", font=("Segoe UI", 20, "bold"),
                 bg=BG, fg=BLUE).pack(pady=(24, 2))
        tk.Label(self, text="Create strong, random passwords instantly",
                 font=("Segoe UI", 9), bg=BG, fg=MUTED).pack(pady=(0, 18))

        # ── Card ──────────────────────────────────────────────────────────────
        card = tk.Frame(self, bg=SURFACE, bd=0)
        card.pack(padx=32, pady=0, fill="x")

        # ── Password display ──────────────────────────────────────────────────
        tk.Label(card, text="Generated Password", font=("Segoe UI", 10),
                 bg=SURFACE, fg=SUBTEXT).pack(anchor="w", padx=20, pady=(20, 4))

        pw_frame = tk.Frame(card, bg=SURFACE2)
        pw_frame.pack(fill="x", padx=20, pady=(0, 4))

        self.password_var = tk.StringVar(value="Click Generate to create a password")
        pw_lbl = tk.Label(pw_frame, textvariable=self.password_var,
                          font=("Consolas", 13), bg=SURFACE2, fg=TEXT,
                          wraplength=360, justify="center", pady=12, padx=12)
        pw_lbl.pack(fill="x")

        # ── Strength bar ──────────────────────────────────────────────────────
        strength_row = tk.Frame(card, bg=SURFACE)
        strength_row.pack(fill="x", padx=20, pady=(6, 0))

        tk.Label(strength_row, text="Strength:", font=("Segoe UI", 9),
                 bg=SURFACE, fg=SUBTEXT).pack(side="left")

        self.strength_label = tk.Label(strength_row, text="—",
                                       font=("Segoe UI", 9, "bold"),
                                       bg=SURFACE, fg=MUTED)
        self.strength_label.pack(side="left", padx=(6, 0))

        self.bar_canvas = tk.Canvas(card, height=6, bg=SURFACE,
                                    highlightthickness=0)
        self.bar_canvas.pack(fill="x", padx=20, pady=(4, 16))

        # ── Separator ─────────────────────────────────────────────────────────
        ttk.Separator(card, orient="horizontal").pack(fill="x", padx=20)

        # ── Length slider ─────────────────────────────────────────────────────
        length_row = tk.Frame(card, bg=SURFACE)
        length_row.pack(fill="x", padx=20, pady=(16, 4))

        tk.Label(length_row, text="Password Length", font=("Segoe UI", 10),
                 bg=SURFACE, fg=SUBTEXT).pack(side="left")

        self.length_var = tk.IntVar(value=16)
        self.length_display = tk.Label(length_row,
                                       textvariable=self.length_var,
                                       font=("Segoe UI", 11, "bold"),
                                       bg=SURFACE, fg=BLUE, width=3)
        self.length_display.pack(side="right")

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TScale", background=SURFACE, troughcolor=SURFACE2,
                        sliderlength=18, sliderrelief="flat")

        self.slider = ttk.Scale(card, from_=4, to=64,
                                variable=self.length_var, orient="horizontal",
                                command=self._on_slider)
        self.slider.pack(fill="x", padx=20, pady=(0, 16))

        # ── Checkboxes ────────────────────────────────────────────────────────
        ttk.Separator(card, orient="horizontal").pack(fill="x", padx=20)
        tk.Label(card, text="Character Types", font=("Segoe UI", 10),
                 bg=SURFACE, fg=SUBTEXT).pack(anchor="w", padx=20, pady=(14, 6))

        checks_frame = tk.Frame(card, bg=SURFACE)
        checks_frame.pack(fill="x", padx=20, pady=(0, 16))

        self.use_upper   = tk.BooleanVar(value=True)
        self.use_lower   = tk.BooleanVar(value=True)
        self.use_digits  = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)

        options = [
            (self.use_upper,   "Uppercase  (A–Z)", LAVENDER),
            (self.use_lower,   "Lowercase  (a–z)", GREEN),
            (self.use_digits,  "Numbers    (0–9)", YELLOW),
            (self.use_symbols, "Symbols  (!@#…)",  PEACH),
        ]

        for i, (var, label, color) in enumerate(options):
            row = i // 2
            col = i % 2
            cb = tk.Checkbutton(
                checks_frame, text=label, variable=var,
                font=("Segoe UI", 10), bg=SURFACE, fg=color,
                activebackground=SURFACE, activeforeground=color,
                selectcolor=SURFACE2, relief="flat", bd=0,
                cursor="hand2", command=self._on_option_change,
            )
            cb.grid(row=row, column=col, sticky="w", padx=(0, 20), pady=3)

        # ── Buttons ───────────────────────────────────────────────────────────
        btn_frame = tk.Frame(card, bg=SURFACE)
        btn_frame.pack(fill="x", padx=20, pady=(4, 20))

        gen_btn = tk.Button(
            btn_frame, text="Generate Password",
            font=("Segoe UI", 11, "bold"),
            bg=BLUE, fg=BG,
            activebackground=LAVENDER, activeforeground=BG,
            relief="flat", bd=0, cursor="hand2", pady=10,
            command=self.generate,
        )
        gen_btn.pack(fill="x", pady=(0, 8))

        self.copy_btn = tk.Button(
            btn_frame, text="Copy to Clipboard",
            font=("Segoe UI", 10),
            bg=SURFACE2, fg=TEXT,
            activebackground="#585b70", activeforeground=TEXT,
            relief="flat", bd=0, cursor="hand2", pady=8,
            command=self._copy,
        )
        self.copy_btn.pack(fill="x")

        # ── Status ────────────────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="")
        tk.Label(self, textvariable=self.status_var,
                 font=("Segoe UI", 8), bg=BG, fg=MUTED).pack(pady=(8, 16))

    # ───────────────────────────────────────────────────── Logic ─────────────

    def _build_charset(self):
        charset = ""
        if self.use_upper.get():   charset += UPPERCASE
        if self.use_lower.get():   charset += LOWERCASE
        if self.use_digits.get():  charset += DIGITS
        if self.use_symbols.get(): charset += SYMBOLS
        return charset

    def generate(self):
        charset = self._build_charset()
        if not charset:
            self.status_var.set("Select at least one character type.")
            return

        length = self.length_var.get()

        # Guarantee at least one char from each selected category
        guaranteed = []
        if self.use_upper.get():   guaranteed.append(random.choice(UPPERCASE))
        if self.use_lower.get():   guaranteed.append(random.choice(LOWERCASE))
        if self.use_digits.get():  guaranteed.append(random.choice(DIGITS))
        if self.use_symbols.get(): guaranteed.append(random.choice(SYMBOLS))

        remaining = [random.choice(charset) for _ in range(length - len(guaranteed))]
        all_chars = guaranteed + remaining
        random.shuffle(all_chars)
        password = "".join(all_chars)

        self.password_var.set(password)
        self._update_strength(password, charset)
        self.status_var.set("")
        self.copy_btn.config(bg=SURFACE2, text="Copy to Clipboard")

    def _copy(self):
        pw = self.password_var.get()
        if not pw or pw == "Click Generate to create a password":
            return
        self.clipboard_clear()
        self.clipboard_append(pw)
        self.copy_btn.config(bg=GREEN, fg=BG, text="Copied!")
        self.after(2000, lambda: self.copy_btn.config(
            bg=SURFACE2, fg=TEXT, text="Copy to Clipboard"))

    def _on_slider(self, _=None):
        # Keep value as integer
        self.length_var.set(int(float(self.slider.get())))

    def _on_option_change(self):
        # Re-generate if a password is already shown
        pw = self.password_var.get()
        if pw and pw != "Click Generate to create a password":
            self.generate()

    # ──────────────────────────────────────────── Strength calculation ────────

    def _entropy(self, password: str, charset_size: int) -> float:
        """Shannon entropy in bits: len * log2(charset_size)."""
        if charset_size <= 1:
            return 0
        return len(password) * math.log2(charset_size)

    def _update_strength(self, password: str, charset: str):
        entropy = self._entropy(password, len(set(charset)))

        if entropy < 28:
            level, color, label = 1, RED,    "Very Weak"
        elif entropy < 36:
            level, color, label = 2, PEACH,  "Weak"
        elif entropy < 60:
            level, color, label = 3, YELLOW, "Fair"
        elif entropy < 80:
            level, color, label = 4, GREEN,  "Strong"
        else:
            level, color, label = 5, BLUE,   "Very Strong"

        self.strength_label.config(text=f"{label}  ({entropy:.0f} bits)", fg=color)
        self._draw_bar(level, color)

    def _draw_bar(self, level: int, color: str):
        self.bar_canvas.update_idletasks()
        w = self.bar_canvas.winfo_width()
        h = 6
        self.bar_canvas.delete("all")
        # Background segments
        seg_w = (w - 8) // 5
        for i in range(5):
            x1 = i * (seg_w + 2)
            x2 = x1 + seg_w
            fill = color if i < level else SURFACE2
            self.bar_canvas.create_rectangle(x1, 0, x2, h, fill=fill,
                                             outline="", width=0)


if __name__ == "__main__":
    app = PasswordGenerator()
    app.mainloop()
