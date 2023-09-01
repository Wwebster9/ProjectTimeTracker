import tkinter as tk
from tkinter import ttk, END


class Timer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # -- variables --
        self.current_time = tk.StringVar(value="00:00:00")
        self.timer_running = False
        self.entry_var = tk.StringVar()

        # -- containers --
        entry_frame = ttk.Frame(self)
        entry_frame.grid(row=0, column=0)

        timer_frame = ttk.Frame(self, height="50")
        timer_frame.grid(row=0, column=1, padx=20, pady=20, sticky="NSEW")

        button_frame = ttk.Frame(self, padding=10)
        button_frame.grid(row=0, column=2, sticky="EW")
        button_frame.columnconfigure("all", weight=1)

        # -- entry field --
        self.timer_entry = ttk.Entry(
            entry_frame,
            textvariable=self.entry_var,
            justify="right",
            width=10,
            font=("Arial", 20)
        )
        self.timer_entry.grid(row=0, column=0, padx=20, pady=20)

        # -- timer field --
        timer_counter = ttk.Label(
            timer_frame,
            textvariable=self.current_time,
            font=("Arial", 20)
        )
        timer_counter.grid(row=0, column=1, pady=(6, 0))

        # -- individual timer buttons --
        self.start_button = ttk.Button(
            button_frame,
            text="Start",
            command=self.start_timer,
            cursor="hand2",
            width=5,
            style="Button.TButton"
        )
        self.start_button.grid(row=0, column=2, sticky="EW", padx=(0, 5))

        self.stop_button = ttk.Button(
            button_frame,
            text="Stop",
            state="disabled",
            command=self.stop_timer,
            cursor="hand2",
            width=5,
            style="Button.TButton"
        )
        self.stop_button.grid(row=0, column=3, sticky="EW", padx=(0, 5))

        self.reset_button = ttk.Button(
            button_frame,
            text="Reset",
            command=self.reset_timer,
            cursor="hand2",
            width=5,
            style="Button.TButton"
        )
        self.reset_button.grid(row=0, column=4, sticky="EW", padx=(0, 5))

        self.clear_button = ttk.Button(
            button_frame,
            text="Clear Entry",
            command=self.clear_entry,
            cursor="hand2",
            style="Button.TButton"
        )
        self.clear_button.grid(row=0, column=5, sticky="EW", padx=(0, 5))

    def start_timer(self):
        self.timer_running = True
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "enabled"
        self.increment_time()

    def stop_timer(self):
        self.timer_running = False
        self.start_button["state"] = "enabled"
        self.stop_button["state"] = "disabled"

    def reset_timer(self):
        self.stop_timer()
        self.current_time.set("00:00:00")

    def clear_entry(self):
        self.timer_entry.delete(0, END)

    def increment_time(self):
        current_time = self.current_time.get()

        if self.timer_running:
            hours, minutes, seconds = current_time.split(":")

            if int(hours) == 99 and int(minutes) == 59 and int(seconds) == 59:
                seconds = 0
                minutes = 0
                hours = 0
            elif int(seconds) == 59 and int(minutes) == 59:
                seconds = 0
                minutes = 0
                hours = int(hours) + 1
            elif int(seconds) == 59:
                seconds = 0
                minutes = int(minutes) + 1
                hours = int(hours)
            else:
                seconds = int(seconds) + 1
                minutes = int(minutes)
                hours = int(hours)

            self.current_time.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.after(1000, self.increment_time)
