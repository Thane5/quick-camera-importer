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

class QuickCameraImporterApp:
    def __init__(self, master=None):
        # 1: Create a builder and setup resources path (if you have images)
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)

        # 2: Load a ui file
        builder.add_from_file(PROJECT_UI)

        # 3: Create the mainwindow
        self.mainwindow = builder.get_object('mainwindow', master)

        # 4: Connect callbacks
        builder.connect_callbacks(self)

        # 5: Apply Windows 11 theme
        sv_ttk.use_dark_theme()
        apply_theme_to_titlebar(self.mainwindow)

        # update text
        self.label_camerastatus = builder.get_variable('var_camerastatus')  # Gets the label's variable
        self.label_camerastatus.set('new text')


    def run(self):
        self.mainwindow.mainloop()


    def update_ui(self):
        #global currentDevice
        #currentDevice = DeviceLink.find_camera()

        if self.camera_okay():
            self.camera_status.config(text=DeviceLink.currentCameraName, foreground="green")
        else:
            self.camera_status.config(text="No Camera Found", foreground="red")
            self.copy_button.state(["disabled"])
            return

        if self.path_okay():
            # we could color the textinput red or something
            pass
        else:
            self.copy_button.state(["disabled"])
            return

        self.copy_button.state(["!disabled"])


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


def open_main_window():
    pass

def apply_theme_to_titlebar(window):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(window, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(window, "dark" if sv_ttk.get_theme() == "dark" else "normal")

if __name__ == "__main__":
    try:
        app = QuickCameraImporterApp()
        app.run()
    except KeyboardInterrupt:
        pass

