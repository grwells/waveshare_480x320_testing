#! /usr/bin/python3
import PySimpleGUI as sg

has_fix = False

interface_column = [[sg.Button("exit")]]

data_column = [
        [
            sg.Table(
                values=[[1000, 2000, 12, 0.69]],
                headings=['N', 'W', '# of satellites', 'HDOP'])
        ]
    ]

layout = [
        [
            sg.Column(data_column),
            sg.VSeparator(),
            sg.Column(interface_column)
        ]
    ]


# Create the window
window = sg.Window(title="ScareCro Provisioner", layout=layout, size=(480, 320))


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "exit" or event == sg.WIN_CLOSED:
        break

window.close()
