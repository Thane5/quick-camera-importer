import os
import win32com.client
import FileHandler


# Define the destination folder where files will be copied
baseDir = r"C:/tmp"  # Update this path
currentCameraName = ""
global currentDevice


def find_camera():
    # Create a DeviceManager object
    wpd_manager = win32com.client.Dispatch("WIA.DeviceManager")

    # List all connected WPD devices
    devices = wpd_manager.DeviceInfos
    if devices.Count == 0:
        print("No MTP devices found.")
        return None

    # Iterate over available devices and process only camera devices
    for device in devices:
        device_type = device.Properties("Type").Value

        # all my cameras return device type 131072, so I will check for that
        if str(device_type) == "131072":
            global currentDevice
            currentDevice = device.Connect()

            global currentCameraName
            currentCameraName = device.Properties("Manufacturer").Value + " " + device.Properties("Name").Value

            print("Using Camera: ", currentCameraName)
            return currentDevice

    currentDevice = None
    currentCameraName = ""
    print("No camera found")
    return None


def copy_files(camera, target_folder):
    if camera is not None:
        try:
            print(camera.Items.Count, "items found")

            for item in camera.Items:
                # Extract relevant properties and copy files
                item_name = item.Properties("Item Name").Value if item.Properties.Exists("Item Name") else "Unnamed Item"
                file_extension = item.Properties("Filename extension").Value if item.Properties.Exists("Filename extension") else "Unknown"
                item_size = item.Properties("Item Size").Value if item.Properties.Exists("Item Size") else "Unknown size"

                # Copy the file to the specified folder
                FileHandler.copy_file_from_camera(item, target_folder)
        except AttributeError as e:
            print(f"Error accessing camera attributes: {e}")
    else:
        print("No camera found to copy files from.")