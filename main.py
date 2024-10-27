import os
import pathlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pygubu
import sv_ttk
import pywinstyles, sys

import DeviceLink

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "MainWindow.ui"

builder = pygubu.Builder()

class QuickCameraImporterApp:

    def __init__(self, master=None):
        open_main_window(self, master)
        self.update_ui()


    def btn_refresh_clicked(self):
        self.update_ui()

    def btn_browse_clicked(self):
        self.browse_folder()

    def btn_copy_clicked(self):
        self.copy_now()


    def update_ui(self):
        self.label_camerastatus = builder.get_object('label_camerastatus')
        self.label_camerastatus_text = builder.get_variable('var_camerastatus')
        self.btn_copy = builder.get_object('btn_copy')
        self.path_entry = builder.get_object('path_entry')

        if self.camera_okay():
            self.label_camerastatus_text.set(DeviceLink.currentCameraName)
            self.label_camerastatus.config(foreground="limegreen")
        else:
            self.label_camerastatus_text.set("No Camera Found")
            self.label_camerastatus.config(foreground="red")
            self.btn_copy.state(["disabled"])
            return

        if self.path_okay():
            # we could color the textinput red or something
            pass
        else:
            self.btn_copy.state(["disabled"])
            return

        self.btn_copy.state(["!disabled"])


    def check_conditions(self):
        if self.camera_okay() and self.path_okay():
            self.btn_copy.state(["!disabled"])
        else:
            self.btn_copy.state(["disabled"])

    def camera_okay(self):
        if DeviceLink.find_camera() is None:
            return False
        return True


    def path_okay(self):
        selected_path = self.path_entry.get()

        if os.path.exists(selected_path):
            print("Path is good!")
            DeviceLink.baseDir = selected_path
            return True

        print("Path does not exist:", selected_path)
        messagebox.showerror("Error", f"Invalid path: {selected_path}")
        return False


    def browse_folder(self):
        selected_path = filedialog.askdirectory()
        if selected_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, selected_path)


    def copy_now(self):
        self.update_ui()
        selected_path = self.path_entry.get()
        print("selected_path:", selected_path)
        DeviceLink.copy_files(DeviceLink.currentDevice, selected_path)


def open_main_window(self=None, master=None):
    # 1: Create a builder and setup resources path (if you have images)
    self.builder = pygubu.Builder()
    builder.add_resource_path(PROJECT_PATH)

    # 2: Load a ui file
    builder.add_from_file(PROJECT_UI)

    # 3: Create the mainwindow
    self.mainwindow = builder.get_object('mainwindow', master)

    # 4: Connect callbacks
    builder.connect_callbacks(self)

    # 5: Apply Windows 11 theme
    sv_ttk.use_dark_theme()

    # 5.1 Apply Windows 11 title bar
    version = sys.getwindowsversion()
    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(self.mainwindow, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(self.mainwindow, "dark" if sv_ttk.get_theme() == "dark" else "normal")


    # set the default path to the user's Pictures folder
    self.path_entry = builder.get_object('path_entry')
    pictures_folder = os.path.join(os.path.expanduser("~"), "Pictures")
    self.path_entry.delete(0, tk.END)
    self.path_entry.insert(0, pictures_folder)

if __name__ == "__main__":
    try:
        QuickCameraImporterApp().mainwindow.mainloop()
    except KeyboardInterrupt:
        pass

