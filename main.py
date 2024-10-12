import PySimpleGUI as sg
import os
import MTPDeviceLink

sg.theme("DarkGrey10")
layout = [[sg.T("")], [sg.Text("Copy pictures to: "), sg.Input(key="-TextField-", default_text = "C:/tmp", expand_x = True), sg.FolderBrowse(key="-IN-")],[sg.Button("Copy Now")]]

###Building Window
window = sg.Window('Quick Camera Importer', layout, size=(640,300))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event=="Exit":
        break
    elif event == "Copy Now":
        selectedPath = values["-TextField-"]

        if os.path.exists(selectedPath):
            print("Path is good!")

            print(selectedPath)
            MTPDeviceLink.baseDir = selectedPath
            MTPDeviceLink.list_and_copy_mtp_devices()
        else:
            print("path is shit ", selectedPath)
