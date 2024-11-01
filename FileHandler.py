import os
import time
import pytz
from exif import Image
import pywintypes
import win32file
import win32con
from datetime import datetime


def get_timestamp_for_path(file):
    try:
        if file.Properties.Exists("Item Time Stamp"):
            timestamp = file.Properties("Item Time Stamp").Value

            if hasattr(timestamp, "Date"):
                return timestamp.Date
    except Exception as e:
        print(f"Error reading date from item: {e}")
    return None


def get_timestamp_minus_offset(file):
    try:
        if file.Properties.Exists("Item Time Stamp"):
            timestamp = file.Properties("Item Time Stamp").Value
            print("timestamp.Date is ", timestamp.Date)

            unix_timestamp = timestamp.Date.timestamp()
            offset_seconds = time.localtime().tm_gmtoff

            # Adjust the Unix timestamp by subtracting the offset
            adjusted_timestamp = unix_timestamp - offset_seconds

            # Convert to a human-readable date and time in UTC
            adjusted_datetime = datetime.utcfromtimestamp(adjusted_timestamp)

            if hasattr(timestamp, "Date"):
                return adjusted_timestamp
    except Exception as e:
        print(f"Error reading date from item: {e}")
    return None


def set_file_times(file_path, timestamp):
    # Convert timestamp to seconds since epoch for os.utime
    timestamp_seconds = timestamp

    # Set access and modified times using os.utime
    os.utime(file_path, (timestamp_seconds, timestamp_seconds))

    # Convert to FILETIME for Windows
    creation_time = pywintypes.Time(timestamp)

    # Create a file handle
    handle = win32file.CreateFile(
        file_path,
        win32con.GENERIC_WRITE,
        0,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL,
        None
    )

    try:
        # Set the file times: creation, last access, last write
        win32file.SetFileTime(handle, creation_time, creation_time, creation_time)
    except Exception as e:
        print(f"Error setting file times: {e}")
    finally:
        win32file.CloseHandle(handle)

def copy_and_organize_file(file, base_destination_folder):
    file_name = file.Properties("Item Name").Value if file.Properties.Exists("Item Name") else "Unnamed_Item"
    file_extension = file.Properties("Filename extension").Value if file.Properties.Exists(
        "Filename extension") else "Unknown"

    # Get the date from EXIF metadata on the device itself
    date_and_time = get_timestamp_for_path(file)
    if not date_and_time:
        print(f"Skipping {file_name}.{file_extension}: Date not available.")
        return

    year, month = date_and_time.strftime("%Y"), date_and_time.strftime("%m")
    destination_folder = os.path.join(base_destination_folder, year, month)
    final_path = os.path.join(destination_folder, f"{file_name}.{file_extension}")

    # Skip copying if the file already exists
    if os.path.exists(final_path):
        print(f"Skipping {final_path}: File already exists.")
        return

    # Ensure destination directory exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy the file directly from the device to the target folder
    try:
        file.Transfer().SaveFile(final_path)
        print(f"Copied: {final_path}", ". Reported timeanddate: ", date_and_time)

        timestamp = get_timestamp_minus_offset(file)
        # Set the file's creation and modified times
        set_file_times(final_path, timestamp)

    except Exception as e:
        print(f"Failed to copy {file_name}.{file_extension}: {e}")
