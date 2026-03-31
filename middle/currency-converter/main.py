import tkinter as tk
from tkinter import ttk, messagebox
import requests
import threading

API_BASE = "https://api.frankfurter.app"

CURRENCY_NAMES = {
    "AUD": "Australian Dollar",
    "BGN": "Bulgarian Lev",
    "BRL": "Brazilian Real",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Renminbi Yuan",
    "CZK": "Czech Koruna",
    "DKK": "Danish Krone",
    "EUR": "Euro",
    "GBP": "British Pound",
    "HKD": "Hong Kong Dollar",
    "HUF": "Hungarian Forint",
    "IDR": "Indonesian Rupiah",
    "ILS": "Israeli New Shekel",
    "INR": "Indian Rupee",
    "ISK": "Icelandic Króna",
    "JPY": "Japanese Yen",
    "KRW": "South Korean Won",
    "MXN": "Mexican Peso",
    "MYR": "Malaysian Ringgit",
    "NOK": "Norwegian Krone",
    "NZD": "New Zealand Dollar",
    "PHP": "Philippine Peso",
    "PLN": "Polish Zloty",
    "RON": "Romanian Leu",
    "SEK": "Swedish Krona",
    "SGD": "Singapore Dollar",
    "THB": "Thai Baht",
    "TRY": "Turkish Lira",
    "USD": "US Dollar",
    "ZAR": "South African Rand",
}


class CurrencyConverter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Currency Converter")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        self.currencies = []
        self.rate_cache = {}
        self._after_id = None

        self._build_ui()
        self._load_currencies()

    # ------------------------------------------------------------------ UI --

    def _build_ui(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Combobox & general
        style.configure(
            "TCombobox",
            fieldbackground="#313244",
            background="#313244",
            foreground="#cdd6f4",
            arrowcolor="#89b4fa",
            selectbackground="#45475a",
            selectforeground="#cdd6f4",
            padding=6,
        )
        style.map("TCombobox", fieldbackground=[("readonly", "#313244")])

        # ── Title ──────────────────────────────────────────────────────────
        title = tk.Label(
            self,
            text="Currency Converter",
            font=("Segoe UI", 20, "bold"),
            bg="#1e1e2e",
            fg="#89b4fa",
        )
        title.pack(pady=(24, 4))

        subtitle = tk.Label(
            self,
            text="Live rates via frankfurter.app",
            font=("Segoe UI", 9),
            bg="#1e1e2e",
            fg="#6c7086",
        )
        subtitle.pack(pady=(0, 20))

        # ── Card frame ─────────────────────────────────────────────────────
        card = tk.Frame(self, bg="#313244", bd=0)
        card.pack(padx=32, pady=0, fill="x")

        # ── Amount input ───────────────────────────────────────────────────
        tk.Label(
            card,
            text="Amount",
            font=("Segoe UI", 10),
            bg="#313244",
            fg="#a6adc8",
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(20, 4))

        vcmd = (self.register(self._validate_input), "%P", "%S")
        self.amount_var = tk.StringVar(value="1")
        self.amount_var.trace_add("write", self._on_change)

        self.amount_entry = tk.Entry(
            card,
            textvariable=self.amount_var,
            font=("Segoe UI", 16),
            bg="#45475a",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief="flat",
            bd=0,
            validate="key",
            validatecommand=vcmd,
            width=22,
        )
        self.amount_entry.grid(
            row=1, column=0, columnspan=3, padx=20, pady=(0, 16), ipady=8
        )

        # ── From currency ──────────────────────────────────────────────────
        tk.Label(
            card,
            text="From",
            font=("Segoe UI", 10),
            bg="#313244",
            fg="#a6adc8",
        ).grid(row=2, column=0, sticky="w", padx=(20, 4), pady=(0, 4))

        self.from_var = tk.StringVar(value="USD")
        self.from_combo = ttk.Combobox(
            card,
            textvariable=self.from_var,
            state="readonly",
            width=22,
            font=("Segoe UI", 11),
        )
        self.from_combo.grid(row=3, column=0, padx=(20, 4), pady=(0, 16), ipady=4)
        self.from_combo.bind("<<ComboboxSelected>>", self._on_change)

        # ── Swap button ────────────────────────────────────────────────────
        tk.Label(card, text="", bg="#313244").grid(row=2, column=1)

        swap_btn = tk.Button(
            card,
            text="⇄",
            font=("Segoe UI", 14, "bold"),
            bg="#89b4fa",
            fg="#1e1e2e",
            activebackground="#b4befe",
            activeforeground="#1e1e2e",
            relief="flat",
            bd=0,
            cursor="hand2",
            width=3,
            command=self._swap,
        )
        swap_btn.grid(row=3, column=1, padx=6, pady=(0, 16))

        # ── To currency ────────────────────────────────────────────────────
        tk.Label(
            card,
            text="To",
            font=("Segoe UI", 10),
            bg="#313244",
            fg="#a6adc8",
        ).grid(row=2, column=2, sticky="w", padx=(4, 20), pady=(0, 4))

        self.to_var = tk.StringVar(value="EUR")
        self.to_combo = ttk.Combobox(
            card,
            textvariable=self.to_var,
            state="readonly",
            width=22,
            font=("Segoe UI", 11),
        )
        self.to_combo.grid(row=3, column=2, padx=(4, 20), pady=(0, 16), ipady=4)
        self.to_combo.bind("<<ComboboxSelected>>", self._on_change)

        # ── Divider ────────────────────────────────────────────────────────
        ttk.Separator(card, orient="horizontal").grid(
            row=4, column=0, columnspan=3, sticky="ew", padx=20
        )

        # ── Result ─────────────────────────────────────────────────────────
        tk.Label(
            card,
            text="Result",
            font=("Segoe UI", 10),
            bg="#313244",
            fg="#a6adc8",
        ).grid(row=5, column=0, columnspan=3, sticky="w", padx=20, pady=(16, 4))

        self.result_var = tk.StringVar(value="—")
        result_lbl = tk.Label(
            card,
            textvariable=self.result_var,
            font=("Segoe UI", 22, "bold"),
            bg="#313244",
            fg="#a6e3a1",
            anchor="w",
        )
        result_lbl.grid(
            row=6, column=0, columnspan=3, sticky="w", padx=20, pady=(0, 6)
        )

        self.rate_label = tk.Label(
            card,
            text="",
            font=("Segoe UI", 9),
            bg="#313244",
            fg="#6c7086",
            anchor="w",
        )
        self.rate_label.grid(
            row=7, column=0, columnspan=3, sticky="w", padx=20, pady=(0, 20)
        )

        # ── Status bar ─────────────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Loading currencies...")
        tk.Label(
            self,
            textvariable=self.status_var,
            font=("Segoe UI", 8),
            bg="#1e1e2e",
            fg="#6c7086",
        ).pack(pady=(10, 16))

    # ---------------------------------------------------------- Data loading --

    def _load_currencies(self):
        def fetch():
            try:
                resp = requests.get(f"{API_BASE}/currencies", timeout=8)
                resp.raise_for_status()
                data = resp.json()
                codes = sorted(data.keys())
                self.after(0, lambda: self._populate_currencies(codes))
            except Exception as e:
                self.after(
                    0,
                    lambda: self.status_var.set(f"Error loading currencies: {e}"),
                )

        threading.Thread(target=fetch, daemon=True).start()

    def _populate_currencies(self, codes):
        self.currencies = codes
        display = [f"{c} – {CURRENCY_NAMES.get(c, c)}" for c in codes]
        self.from_combo["values"] = display
        self.to_combo["values"] = display

        # Set defaults
        self._set_combo(self.from_combo, self.from_var, "USD")
        self._set_combo(self.to_combo, self.to_var, "EUR")

        self.status_var.set(f"{len(codes)} currencies loaded")
        self._convert()

    def _set_combo(self, combo, var, code):
        display = [f"{c} – {CURRENCY_NAMES.get(c, c)}" for c in self.currencies]
        for item in display:
            if item.startswith(code):
                var.set(item)
                return
        if display:
            var.set(display[0])

    # ----------------------------------------------------------- Conversion --

    def _on_change(self, *_):
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(300, self._convert)

    def _convert(self):
        raw = self.amount_var.get().strip()
        if not raw:
            self.result_var.set("—")
            self.rate_label.config(text="")
            return

        try:
            amount = float(raw)
        except ValueError:
            self.result_var.set("Invalid input")
            self.rate_label.config(text="")
            return

        from_code = self.from_var.get().split(" – ")[0]
        to_code = self.to_var.get().split(" – ")[0]

        if not from_code or not to_code:
            return

        if from_code == to_code:
            self.result_var.set(f"{amount:,.2f} {to_code}")
            self.rate_label.config(text="Same currency — rate is 1.00")
            return

        cache_key = f"{from_code}_{to_code}"
        if cache_key in self.rate_cache:
            rate = self.rate_cache[cache_key]
            self._display_result(amount, rate, from_code, to_code, cached=True)
        else:
            self.status_var.set("Fetching rate...")
            threading.Thread(
                target=self._fetch_rate,
                args=(amount, from_code, to_code),
                daemon=True,
            ).start()

    def _fetch_rate(self, amount, from_code, to_code):
        try:
            url = f"{API_BASE}/latest?amount=1&from={from_code}&to={to_code}"
            resp = requests.get(url, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            rate = data["rates"][to_code]
            self.rate_cache[f"{from_code}_{to_code}"] = rate
            self.after(
                0, lambda: self._display_result(amount, rate, from_code, to_code)
            )
        except Exception as e:
            self.after(0, lambda: self.status_var.set(f"API error: {e}"))

    def _display_result(self, amount, rate, from_code, to_code, cached=False):
        converted = round(amount * rate, 2)
        self.result_var.set(f"{converted:,.2f} {to_code}")
        self.rate_label.config(
            text=f"1 {from_code} = {rate:.6f} {to_code}"
            + ("  (cached)" if cached else "")
        )
        self.status_var.set("Rate updated successfully")

    # ---------------------------------------------------------------- Swap --

    def _swap(self):
        from_val = self.from_var.get()
        to_val = self.to_var.get()
        self.from_var.set(to_val)
        self.to_var.set(from_val)
        self.rate_cache.clear()
        self._convert()

    # ─────────────────────────────────────── Input validation (max 9 digits) --

    def _validate_input(self, new_value, inserted_char):
        if new_value == "":
            return True

        # Allow only digits and one decimal point
        allowed = set("0123456789.")
        if inserted_char not in allowed:
            self.bell()
            return False

        # Prevent more than one decimal point
        if new_value.count(".") > 1:
            self.bell()
            return False

        # Max 9 digits (excluding decimal point)
        digits_only = new_value.replace(".", "")
        if len(digits_only) > 9:
            self.bell()
            return False

        return True


if __name__ == "__main__":
    app = CurrencyConverter()
    app.mainloop()
