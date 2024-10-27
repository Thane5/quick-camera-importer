import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sv_ttk
import pywinstyles, sys

import DeviceLink

class QuickCameraImporterApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Quick Camera Importer")
        self.root.geometry("640x300")

        # Apply a theme (optional, adjust as needed)
        self.style = ttk.Style()
        #self.style.theme_use("clam")  # Try "alt", "default", "classic" or any theme available on your system
        sv_ttk.use_dark_theme()

        self.create_widgets()
        self.update_ui()  # Initial update to set the camera status

        # Add a close event handler to ensure proper cleanup
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.root.quit()
        self.root.destroy()

    def create_widgets(self):
        # Camera Panel
        camera_frame = ttk.Frame(self.root, padding=(10, 5))
        camera_frame.pack(pady=(20, 0), fill='x')

        camera_label = ttk.Label(camera_frame, text="Selected Camera:")
        camera_label.pack(side="left", padx=(10, 5))

        self.camera_status = ttk.Label(camera_frame, text="No Camera Found", foreground="red",
                                       font=("Helvetica", 12, "bold"))
        self.camera_status.pack(side="left", expand=True, fill="x")

        self.check_camera_button = ttk.Button(camera_frame, text="Check Connection", command=self.update_ui)
        self.check_camera_button.pack(side="right", padx=10)

        # Path Panel
        path_frame = ttk.Frame(self.root, padding=(10, 5))
        path_frame.pack(pady=(20, 0), fill='x')

        path_label = ttk.Label(path_frame, text="Copy pictures to:")
        path_label.pack(side="left", padx=(10, 5))

        self.path_entry = ttk.Entry(path_frame)
        self.path_entry.insert(0, "C:/tmp")
        self.path_entry.pack(side="left", fill="x", expand=True)

        self.browse_button = ttk.Button(path_frame, text="Browse", command=self.browse_folder)
        self.browse_button.pack(side="right", padx=10)

        # Copy Now Button
        self.copy_button = ttk.Button(self.root, text="Copy Now", command=self.copy_now, state="disabled", width=20)
        self.copy_button.pack(pady=20)


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
        print("i am camera_okaycamera_okay")

        if DeviceLink.find_camera() is None:
            print("camera_okaycamera_okay returns False")
            return False

        print("camera_okaycamera_okay returns True")
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


def apply_theme_to_titlebar(window):
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Set the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(window, "#1c1c1c" if sv_ttk.get_theme() == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(window, "dark" if sv_ttk.get_theme() == "dark" else "normal")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = QuickCameraImporterApp(root)
        apply_theme_to_titlebar(root)
        root.mainloop()
    except KeyboardInterrupt:
        pass

