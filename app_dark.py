import tkinter as tk
import pandas as pd
import datetime
from tkinter import ttk
from tkinter.messagebox import askokcancel, showerror
from tkinter.filedialog import asksaveasfilename
from timer import Timer
from windows import set_dpi_awareness
import sv_ttk

set_dpi_awareness()


class ProjectTimeTracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- styling --
        sv_ttk.set_theme("dark")
        style = ttk.Style()
        style.configure("Button.TButton", font=("Arial", 12))

        # -- variables --
        self.number_timers = 3  # default to three timers
        self.timers = []

        self.title("Project Time Tracker")  # set title of app
        self.resizable(width=True, height=False)  # resizable only horizontally
        self.columnconfigure(0, weight=1)  # allows the contents to stay centered when resizing the window
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)  # calls the confirm exit function when closing the window

        # -- containers --
        timer_container = ttk.Frame(self)
        timer_container.grid(row=0, column=0)

        button_container = ttk.Frame(self)
        button_container.grid(row=1, column=0, pady=(0, 20))

        # -- global buttons --
        add_timer_button = ttk.Button(
            button_container,
            text="Add Timer",
            command=self.add_timer,
            style="Button.TButton"
        )
        add_timer_button.grid(row=0, column=0, sticky="EW", padx=(0, 5))

        reset_all_button = ttk.Button(
            button_container,
            text="Reset All",
            command=self.reset_all_timers,
            style="Button.TButton"
        )
        reset_all_button.grid(row=0, column=1, sticky="EW", padx=(0, 5))

        clear_all_button = ttk.Button(
            button_container,
            text="Clear All Entries",
            command=self.clear_all_entries,
            style="Button.TButton"
        )
        clear_all_button.grid(row=0, column=2, sticky="EW", padx=(0, 5))

        excel_export_button = ttk.Button(
            button_container,
            text="Export to Excel",
            command=self.export_to_excel,
            style="Button.TButton"
        )
        excel_export_button.grid(row=0, column=3, sticky="EW", padx=(0, 5))

        # -- timers --
        # only add three timers to start off with
        timer1 = Timer(timer_container)
        timer1.grid(row=0, column=0, sticky="NSEW")
        self.timers.append(timer1)
        timer2 = Timer(timer_container)
        timer2.grid(row=1, column=0, sticky="NSEW")
        self.timers.append(timer2)
        timer3 = Timer(timer_container)
        timer3.grid(row=2, column=0, sticky="NSEW")
        self.timers.append(timer3)
        timer4 = Timer(timer_container)
        self.timers.append(timer4)
        timer5 = Timer(timer_container)
        self.timers.append(timer5)
        timer6 = Timer(timer_container)
        self.timers.append(timer6)
        timer7 = Timer(timer_container)
        self.timers.append(timer7)
        timer8 = Timer(timer_container)
        self.timers.append(timer8)
        timer9 = Timer(timer_container)
        self.timers.append(timer9)
        timer10 = Timer(timer_container)
        self.timers.append(timer10)

    def add_timer(self):
        if self.number_timers < 10:
            self.timers[self.number_timers].grid(row=self.number_timers, column=0, sticky="NSEW")
            self.number_timers += 1

    def reset_all_timers(self):
        for timer in self.timers:
            timer.reset_timer()

    def clear_all_entries(self):
        for timer in self.timers:
            timer.clear_entry()

    def export_to_excel(self):
        excel_dict = {}
        try:
            current_date = str(datetime.date.today())  # grab current date (YYYY-MM-DD)
            file_name = current_date + "_Time Entries.xlsx"  # create file name with current date
            file_path = asksaveasfilename(
                confirmoverwrite=True,
                defaultextension=".xlsx",
                filetypes=[("Excel Workbook", "*.xlsx")],
                initialfile=file_name
            )
            for timer in self.timers:
                if timer.entry_var.get() == "" and timer.current_time.get() == "00:00:00":
                    continue
                if timer.entry_var.get() in excel_dict:
                    showerror(
                        title="Error",
                        message="Duplicate project # in entry fields. Please correct and try again."
                    )
                    return
                excel_dict[timer.entry_var.get()] = timer.current_time.get()
            # create a new dictionary for updating numeric strings to integers. this is done to prevent errors when
            # numeric strings are inserted into Excel (they show up with a green triangle and error message in Excel)
            clean_excel_dict = {}
            for key, value in excel_dict.items():
                if key.isnumeric():
                    clean_excel_dict[int(key)] = value
                else:
                    clean_excel_dict[key] = value
            df = pd.DataFrame(data=clean_excel_dict, index=["Time"]).T  # create dataframe and transpose
            df.to_excel(file_path, index_label="Project#", sheet_name=current_date)  # create Excel file
        except PermissionError:  # error generated when file is open when trying to overwrite
            # display message to user to close the Excel file
            showerror(
                title="Permission denied",
                message="Unable to save. Please close Excel file first before exporting."
            )
        except ValueError:
            # ValueError generated if user does not select a location to save Excel file. Do nothing if no file
            # location is selected
            pass

    def confirm_exit(self):
        # display confirmation message to user to avoid accidentally quitting application
        if askokcancel(title="Quit", message="Do you want to quit?"):
            self.destroy()


app = ProjectTimeTracker()
app.mainloop()
