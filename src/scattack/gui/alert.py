from tkinter import ttk
import tkinter


class AlertWindow(tkinter.Toplevel):
    def __init__(self, *args, message: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = ttk.Label(self, text=message)
        self.label.pack(padx=20, pady=20)
