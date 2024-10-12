import os
import win32com.client
import FileHandler


# Define the destination folder where files will be copied
baseDir = r"C:/tmp"  # Update this path

def is_camera_device(device):
    # Check if the device name contains "Camera"
    device_name = device.Properties("Name").Value
    return "Camera" in device_name or "X-T30" in device_name  # Add more camera names if needed


def list_and_copy_mtp_devices():
    # Create a DeviceManager object
    wpd_manager = win32com.client.Dispatch("WIA.DeviceManager")

    # List all connected WPD devices
    devices = wpd_manager.DeviceInfos
    if devices.Count == 0:
        print("No MTP devices found.")
        return

    # Iterate over available devices and process only camera devices
    for device in devices:
        device_name = device.Properties("Name").Value
        if is_camera_device(device):
            print(f"Camera found: {device_name}")

            # Connect to the camera
            wia_device = device.Connect()

            # List files or folders on the camera
            print(f"Listing and copying files from device: {device_name}")
            for item in wia_device.Items:
                # Extract relevant properties and copy files
                item_name = item.Properties("Item Name").Value if item.Properties.Exists("Item Name") else "Unnamed Item"
                file_extension = item.Properties("Filename extension").Value if item.Properties.Exists("Filename extension") else "Unknown"

                # Copy the file to the specified folder
                FileHandler.copy_file_from_camera(item, baseDir)
        else:
            print(f"Skipping non-camera device: {device_name}")

    print("Done.")
