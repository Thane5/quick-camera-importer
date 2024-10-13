import PySimpleGUI as sg
import os
import MTPDeviceLink

sg.theme("DarkGrey10")

cameraPanel = [
    sg.Text("Selected Camera: "),
    sg.Text("No Camera Found", key="txt_camera", text_color="red", font=("Helvetiva", 12, "bold"), expand_x = True),
    sg.Button("Check Connection", key="btn_checkCamera", size=(15,1))
]

pathPanel = [
    sg.Text("Copy pictures to: "),
    sg.Input(key="-TextField-", default_text = "C:/tmp", expand_x = True),
    sg.FolderBrowse(key="-IN-", size=(15,1))
]

layout = [
    [sg.T("")],
    cameraPanel,
    [sg.T("")],
    pathPanel,
    [sg.VPush()],
    [sg.Push(), sg.Button("Copy Now", key="btn_copy", size=(20,2)), sg.Push()],
    [sg.VPush()]
]

###Building Window
window = sg.Window('Quick Camera Importer', layout, size=(640,300))

while True:
    try:
        event, values = window.read()
    except KeyboardInterrupt:
        exit(0)

    if event == "btn_checkCamera":
        MTPDeviceLink.find_camera()
        #print(MTPDeviceLink.currentCameraName)
        if MTPDeviceLink.currentCameraName == "":
            window["txt_camera"].update("No Camera Found", text_color="red")
            window["btn_copy"].update(disabled=True)
        else:
            window['txt_camera'].update(MTPDeviceLink.currentCameraName, text_color="green")
            window["btn_copy"].update(disabled=False)

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

# todo: add display and refresh button for detected camera
# todo: only copy when camera is found and target path exists
# todo: add progress bar