import os
import pywintypes
import win32file
import win32con
from datetime import datetime, timezone, timedelta


def format_date(timestamp):
    # Format the timestamp directly if it's a datetime object
    if isinstance(timestamp, datetime):
        year = timestamp.strftime("%Y")  # Get the year
        month = timestamp.strftime("%m")  # Get the month
        return year, month  # Return both year and month
    return "Unknown_Date", "Unknown_Date"

def set_file_times(file_path, timestamp):
    # Convert the UTC timestamp to your local time by subtracting the offset
    # Assuming you're UTC+2, we subtract 2 hours
    local_offset = timedelta(hours=2)
    print("timeoffset", datetime.utcoffset(timestamp))
    local_timestamp = timestamp - local_offset  # Convert UTC to local time

    # Convert the timestamp to a format that os.utime can accept (seconds since epoch)
    timestamp_seconds = local_timestamp.timestamp()

    # Update access and modification times
    os.utime(file_path, (timestamp_seconds, timestamp_seconds))

    # Convert the local timestamp to a pywintypes time object
    creation_time = pywintypes.Time(local_timestamp)

    handle = win32file.CreateFile(
        file_path,
        win32con.GENERIC_WRITE,
        0,  # No sharing
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL,
        None
    )

    try:
        # Set the creation time
        win32file.SetFileTime(handle, creation_time, None, None)
        print(f"Successfully set creation time for {file_path}")
    except Exception as e:
        print(f"Error setting creation time: {e}")
    finally:
        win32file.CloseHandle(handle)

def get_timestamp(item):
    # Extract the timestamp from the item
    if item.Properties.Exists("Item Time Stamp"):
        timestamp = item.Properties("Item Time Stamp").Value
        print(f"Raw Timestamp: {timestamp}, Type: {type(timestamp)}")  # Debug print

        # Attempt to access the 'Date' property
        try:
            if hasattr(timestamp, 'Date'):
                date_value = timestamp.Date
                print(f"Date Property: {date_value}")  # Debug print
                return date_value  # Return the date if it's in a usable format

            if hasattr(timestamp, 'String'):
                string_value = timestamp.String
                print(f"String Property: {string_value}")  # Debug print
                # We may need to parse the string if it contains a date
                return string_value  # Just return the string for now

        except Exception as e:
            print(f"Error accessing timestamp properties: {e}")

    return None

def copy_file_from_camera(item, base_destination_folder):
    # Get the creation timestamp
    timestamp = get_timestamp(item)
    year, month = format_date(timestamp) if timestamp else ("Unknown_Date", "Unknown_Date")

    # Print the year and month for debugging
    print(f"Year: {year}, Month: {month}")  # Debug print

    # Create the destination path based on the year and month
    destination_folder = os.path.join(base_destination_folder, year, month)

    # Create the destination file path
    item_name = item.Properties("Item Name").Value if item.Properties.Exists("Item Name") else "Unnamed Item"
    file_extension = item.Properties("Filename extension").Value if item.Properties.Exists("Filename extension") else "Unknown"
    destination_file = os.path.join(destination_folder, f"{item_name}.{file_extension}")

    # Check if the destination folder exists, if not, create it
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Check if the item is an image file and save it using SaveFile
    try:
        if item.Properties.Exists("Item Size") and item.Properties("Item Size").Value > 0:
            # Using the SaveFile method to save the item directly
            image_file = item.Transfer()  # Transfer to an ImageFile object
            image_file.SaveFile(destination_file)
            print(f"Copied: {destination_file}")

            # Set the file's creation and last modified times
            if timestamp:
                set_file_times(destination_file, timestamp)

        else:
            print(f"Skipping {item_name}.{file_extension}: Not a valid image file.")
    except Exception as e:
        print(f"Failed to copy {item_name}.{file_extension}: {e}")