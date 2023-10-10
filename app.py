import tkinter as tk
import pandas as pd
import datetime
from tkinter import ttk
from tkinter.messagebox import askokcancel, showerror
from tkinter.filedialog import asksaveasfilename
from timer import Timer
from windows import set_dpi_awareness
import sv_ttk

set_dpi_awareness()  # set high DPI awareness


class ProjectTimeTracker(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -- styling --
        sv_ttk.set_theme("dark")  # set theme to dark
        style = ttk.Style()  # create style object
        style.configure("Button.TButton", font=("Arial", 10))  # configure style for buttons

        # -- variables --
        self.number_timers = 3  # number of timers currently displayed (default is 3)
        self.timers = []  # list to hold timer objects

        # -- window configuration --
        self.title("Project Time Tracker")  # set window title
        self.resizable(width=True, height=False)  # allow window to be resized horizontally only
        self.columnconfigure(0, weight=1)  # allow the window to stay centered when resized
        self.protocol("WM_DELETE_WINDOW", self.confirm_exit)  # display confirmation message when user tries to quit

        # -- containers --
        timer_container = ttk.Frame(self)
        timer_container.grid(row=0, column=0)

        button_container = ttk.Frame(self)
        button_container.grid(row=1, column=0, pady=(0, 20))

        # -- global buttons --
        add_timer_button = ttk.Button(button_container,
                                      text="Add Timer",
                                      command=self.add_timer,
                                      style="Button.TButton")
        add_timer_button.grid(row=0, column=0, sticky="EW", padx=(0, 5))

        reset_all_button = ttk.Button(button_container,
                                      text="Reset All",
                                      command=self.reset_all_timers,
                                      style="Button.TButton")
        reset_all_button.grid(row=0, column=1, sticky="EW", padx=(0, 5))

        clear_all_button = ttk.Button(button_container,
                                      text="Clear All Entries",
                                      command=self.clear_all_entries,
                                      style="Button.TButton")
        clear_all_button.grid(row=0, column=2, sticky="EW", padx=(0, 5))

        excel_export_button = ttk.Button(button_container,
                                         text="Export to Excel",
                                         command=self.export_to_excel,
                                         style="Button.TButton")
        excel_export_button.grid(row=0, column=3, sticky="EW", padx=(0, 5))

        # -- timers --
        # create 10 timer objects and add to list. Only display first 3 timers
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

        # bind any key pressed to call the text_entry_limit function to limit text entry to 256 characters
        self.text_entry = None
        ProjectTimeTracker.bind(self, "<Key>", self.text_entry_limit)

    def text_entry_limit(self, event):
        """Limit text entry field to 256 characters"""
        try:
            self.text_entry = event.widget
            if len(self.text_entry.get("0.0", "end-1c")) > 256:
                self.text_entry.delete("end-2c", "end-1c")
        except TypeError:
            # TypeError generated if event.widget is not a text entry field. Do nothing if event.widget is not a text
            # entry field
            pass
        except AttributeError:
            # AttributeError generated when cursor is not within a text field and the user presses a key. Do nothing
            # if cursor is not within a text entry field
            pass

    def add_timer(self):
        """Add timer to window"""
        # only add timer if number of timers is less than 10
        if self.number_timers < 10:
            self.timers[self.number_timers].grid(row=self.number_timers, column=0, sticky="NSEW")
            self.number_timers += 1

    def reset_all_timers(self):
        """Reset all timers"""
        for timer in self.timers:
            timer.reset_timer()

    def clear_all_entries(self):
        """Clear all entries"""
        for timer in self.timers:
            timer.clear_entry()

    def export_to_excel(self):
        """Export time entries to Excel file"""
        # create dictionary to hold time entries
        excel_dict = {"Project #": [],  #
                      "Time": [],
                      "Description": []}
        try:
            current_date = str(datetime.date.today())  # get current date
            file_name = current_date + "_Time Entries.xlsx"  # create file name with current date

            # ask user to select location to save Excel file
            file_path = asksaveasfilename(confirmoverwrite=True,
                                          defaultextension=".xlsx",
                                          filetypes=[("Excel Workbook", "*.xlsx")],
                                          initialfile=file_name)

            for timer in self.timers:
                # only add time entries to dictionary if project # and time are not empty
                if timer.project_num.get() == "" and timer.current_time.get() == "00:00:00":
                    continue
                # display error message if project # is duplicate (includes empty project #'s)
                if timer.project_num.get() in excel_dict:
                    showerror(title="Error",
                              message="Duplicate project # in entry fields. Please correct and try again.")
                    return

                # append project # and time to dictionary
                excel_dict["Project #"].append(timer.project_num.get())
                excel_dict["Time"].append(timer.current_time.get())
                # append description to dictionary. Use "end-1c" to remove newline character at end of text
                excel_dict["Description"].append(timer.text_entry.get("0.0", "end-1c"))

            # create dataframe from dictionary and export to Excel file
            df = pd.DataFrame(data=excel_dict, index=None)
            writer = pd.ExcelWriter(file_path, engine="xlsxwriter")  # create ExcelWriter object
            df.to_excel(writer, index=False, sheet_name=current_date)  # write dataframe to Excel file
            worksheet = writer.sheets[current_date]  # get worksheet object from workbook object

            # set column widths automatically
            for idx, col in enumerate(df.columns):
                series = df[col]
                max_len = max((series.astype(str).map(len).max(),  # length of largest item
                               len(str(series.name))  # length of column name/header
                               ))
                worksheet.set_column(idx, idx, max_len)  # set column width
            writer.close()  # close ExcelWriter object

        except PermissionError:  # PermissionError generated if user tries to save Excel file while it is open
            showerror(title="Permission denied",
                      message="Unable to save. Please close Excel file first before exporting.")
        except ValueError:
            # ValueError generated if user does not select a location to save Excel file. Do nothing if no file
            # location is selected
            pass

    def confirm_exit(self):
        # display confirmation message when user tries to quit
        if askokcancel(title="Quit", message="Do you want to quit?"):
            self.destroy()


app = ProjectTimeTracker()
app.mainloop()
