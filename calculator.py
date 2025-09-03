import tkinter as tk
from tkinter import font


class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("300x450")
        self.resizable(False, False)
        self.configure(bg="#2E2E2E")

        # Custom font
        self.custom_font = font.Font(family="Helvetica", size=18)

        # Variables
        self.current_input = tk.StringVar(value="0")
        self.operation = None
        self.stored_value = 0
        self.reset_screen = False

        self._create_ui()

    def _create_ui(self):
        # Display
        display_frame = tk.Frame(self, bg="#2E2E2E")
        display_frame.pack(pady=(20, 10), padx=10, fill="x")

        display = tk.Entry(
            display_frame,
            textvariable=self.current_input,
            font=self.custom_font,
            borderwidth=0,
            relief="flat",
            justify="right",
            bg="#3D3D3D",
            fg="white",
            insertbackground="white"
        )
        display.pack(fill="x", ipady=10)

        # Button grid
        buttons = [
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('C', '0', '=', '+')
        ]

        button_frame = tk.Frame(self, bg="#2E2E2E")
        button_frame.pack(padx=10, pady=10, fill="both", expand=True)

        for i, row in enumerate(buttons):
            for j, symbol in enumerate(row):
                btn = tk.Button(
                    button_frame,
                    text=symbol,
                    font=self.custom_font,
                    bg="#4A4A4A",
                    fg="white",
                    activebackground="#5E5E5E",
                    activeforeground="white",
                    borderwidth=0,
                    relief="flat",
                    command=lambda s=symbol: self._on_button_click(s)
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
                button_frame.grid_columnconfigure(j, weight=1)
            button_frame.grid_rowconfigure(i, weight=1)

    def _on_button_click(self, symbol):
        current = self.current_input.get()

        if symbol in '0123456789':
            if current == '0' or self.reset_screen:
                self.current_input.set(symbol)
                self.reset_screen = False
            else:
                self.current_input.set(current + symbol)

        elif symbol == 'C':
            self.current_input.set("0")
            self.stored_value = 0
            self.operation = None

        elif symbol in '+-*/':
            if self.operation and not self.reset_screen:
                self._calculate()
            self.stored_value = float(current)
            self.operation = symbol
            self.reset_screen = True

        elif symbol == '=':
            if self.operation:
                self._calculate()
                self.operation = None

    def _calculate(self):
        try:
            current = float(self.current_input.get())
            if self.operation == '+':
                result = self.stored_value + current
            elif self.operation == '-':
                result = self.stored_value - current
            elif self.operation == '*':
                result = self.stored_value * current
            elif self.operation == '/':
                result = self.stored_value / current

            self.current_input.set(str(result))
            self.stored_value = result
            self.reset_screen = True
        except ZeroDivisionError:
            self.current_input.set("Error")
            self.reset_screen = True


if __name__ == "__main__":
    app = Calculator()
    app.mainloop()