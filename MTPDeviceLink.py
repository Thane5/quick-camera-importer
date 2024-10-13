import os
import win32com.client
import FileHandler


# Define the destination folder where files will be copied
baseDir = r"C:/tmp"  # Update this path
currentCameraName = ""
global currentDevice

def is_camera_device(device):
    # Check if the device name contains "Camera"
    device_name = device.Properties("Name").Value
    return "Camera" in device_name or "X-T30" in device_name  # Add more camera names if needed


def list_and_copy_mtp_devices():
    FileHandler.copy_file_from_camera(item, baseDir)

def find_camera():

    # Create a DeviceManager object
    wpd_manager = win32com.client.Dispatch("WIA.DeviceManager")

    # List all connected WPD devices
    devices = wpd_manager.DeviceInfos
    if devices.Count == 0:
        print("No MTP devices found.")
        return

    allDevices = []

    # Iterate over available devices and process only camera devices
    for device in devices:
        if is_camera_device(device):
            print(device.Properties("Manufacturer").Value + " " + device.Properties("Name").Value)

            # Connect to the camera
            wia_device = device.Connect()

            allDevices.append(device)
        else:
            #print(f"Skipping non-camera device: {device_name}")
            pass

    if allDevices:
        global currentDevice
        currentDevice = allDevices[0]

        global currentCameraName
        currentCameraName = currentDevice.Properties("Manufacturer").Value + " " + currentDevice.Properties("Name").Value

        print("Using Camera: ", currentCameraName)
    else:
        currentCameraName = ""
        print("No camera found")