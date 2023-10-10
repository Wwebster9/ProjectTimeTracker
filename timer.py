import tkinter as tk
from tkinter import ttk
import customtkinter as ctk


class Timer(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # -- variables --
        self.current_time = tk.StringVar(value="00:00:00")
        self.timer_running = False
        self.project_num = tk.StringVar()

        # -- project # frame and entry field --
        proj_num_entry_frame = ttk.Frame(self)
        proj_num_entry_frame.grid(row=0, column=0, padx=(20, 0), pady=15)

        self.proj_num_title = ttk.Label(proj_num_entry_frame, text="Project No.", font=("Arial", 10))
        self.proj_num_title.grid(row=0, column=0)

        self.proj_num_entry = ctk.CTkEntry(proj_num_entry_frame,
                                           border_width=2,
                                           fg_color="#272727",
                                           textvariable=self.project_num,
                                           text_color="#FFFFFF",
                                           justify="center",
                                           width=150,
                                           height=46,
                                           font=("Arial", 20))
        self.proj_num_entry.grid(row=1, column=0)

        # -- description frame and text field --
        description_frame = ttk.Frame(self)
        description_frame.grid(row=0, column=1, padx=(20, 0), pady=15)

        self.descr_field_title = ttk.Label(description_frame, text="Description", font=("Arial", 10))
        self.descr_field_title.grid(row=0, column=0)

        self.text_entry = ctk.CTkTextbox(description_frame,
                                         border_width=2,
                                         height=46,
                                         width=250,
                                         text_color="#FFFFFF",
                                         fg_color="#272727",
                                         wrap="word",
                                         font=("Arial", 12))
        self.text_entry.grid(row=1, column=0, sticky='EW')

        timer_frame = ttk.Frame(self, height="50")
        timer_frame.grid(row=0, column=2, padx=20, pady=15, sticky="NSEW")

        self.timer_label = ttk.Label(timer_frame, text="Timer", font=("Arial", 10))
        self.timer_label.grid(row=0, column=0)

        timer_counter = ttk.Label(timer_frame, textvariable=self.current_time, font=("Arial", 20))
        timer_counter.grid(row=1, column=0, pady=(7, 0))

        # -- button frame and individual timer buttons --
        button_frame = ttk.Frame(self)
        button_frame.grid(row=0, column=3, sticky="EW")
        button_frame.columnconfigure("all", weight=1)

        self.blank_label = ttk.Label(button_frame, text="")
        self.blank_label.grid(row=0, column=0)

        self.start_button = ttk.Button(button_frame,
                                       text="Start",
                                       command=self.start_timer,
                                       cursor="hand2",
                                       width=5,
                                       style="Button.TButton")
        self.start_button.grid(row=1, column=0, sticky="EW", padx=(0, 5))

        self.stop_button = ttk.Button(button_frame,
                                      text="Stop",
                                      state="disabled",
                                      command=self.stop_timer,
                                      cursor="hand2",
                                      width=5,
                                      style="Button.TButton")
        self.stop_button.grid(row=1, column=1, sticky="EW", padx=(0, 5))

        self.reset_button = ttk.Button(button_frame,
                                       text="Reset",
                                       command=self.reset_timer,
                                       cursor="hand2",
                                       width=5,
                                       style="Button.TButton")
        self.reset_button.grid(row=1, column=2, sticky="EW", padx=(0, 5))

        self.add_15m_button = ttk.Button(button_frame,
                                         text="Add 15m",
                                         command=self.add_15_minutes,
                                         cursor="hand2",
                                         style="Button.TButton")
        self.add_15m_button.grid(row=1, column=3, sticky="EW", padx=(0, 5))

        self.clear_button = ttk.Button(button_frame,
                                       text="Clear Entry",
                                       command=self.clear_entry,
                                       cursor="hand2",
                                       style="Button.TButton")
        self.clear_button.grid(row=1, column=4, sticky="EW", padx=(0, 20))

    def start_timer(self):
        """Starts the timer and disables the start button"""
        self.timer_running = True
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "enabled"
        self.increment_time()

    def stop_timer(self):
        """Stops the timer and disables the stop button"""
        self.timer_running = False
        self.start_button["state"] = "enabled"
        self.stop_button["state"] = "disabled"

    def reset_timer(self):
        """Resets the timer to 00:00:00"""
        self.stop_timer()
        self.current_time.set("00:00:00")

    def add_15_minutes(self):
        """Adds 15 minutes to the current time"""
        hours, minutes, seconds = self.current_time.get().split(":")
        if (int(minutes) + 15) >= 60:
            minutes = (int(minutes) + 15) - 60
            hours = int(hours) + 1
        else:
            minutes = int(minutes) + 15
        self.current_time.set(f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")

    def clear_entry(self):
        """Clears the project number and description entry fields"""
        self.proj_num_entry.delete(0, "end")
        self.text_entry.delete("0.0", "end")

    def increment_time(self):
        """Increments the timer by 1 second while timer is running"""
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
