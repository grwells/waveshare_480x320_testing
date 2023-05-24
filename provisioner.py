#! /usr/bin/python3
import PySimpleGUI as sg
import random
sg.theme("dark grey 9")

has_fix = False
data_visible = False

val = 0

interface_column = [
        [
            sg.Button("exit"),
            sg.Button("clear"),
            sg.Button('increment', visible=True)
        ]
    ]

data_column = [
        [
            sg.Frame(
                    'Latitude',
                    [[sg.Text(1000.0000, key='lat_text')]],
                    key='lat_frame'
                ),
            sg.Frame(
                    'Longitude',
                    [[sg.Text(1200.0000, key='long_text')]],
                    key='long_frame'
                ),
            sg.Frame(
                    'HDOP',
                    [[sg.Text(0.69, key='hdop_text')]],
                    key='hdop_frame'
                ),
            sg.Frame(
                    'Satellites',
                    [[sg.Text(12, key='sat_text')]],
                    key='sat_frame'
                ),
        ],
        [
            sg.Button('update'),
        ]
    ]

layout = [
        [
            sg.Frame('Data', data_column, k='-KEY-data_col', visible=False),
            sg.ProgressBar(
                100,
                orientation='horizontal',
                border_width='10',
                key='-KEY-fix_prog',
                visible=True),
        ],
        [
            sg.Column(interface_column)
        ]
    ]

cleared_window_layout = [[]]

# Create the window
window = sg.Window(
        title="ScareCro Provisioner", 
        no_titlebar=True,
        alpha_channel=0.7,
        layout=layout, size=(480, 320),
    )


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "exit" or event == sg.WIN_CLOSED:
        break

    if event == "clear":
        print('clearing')
        data_visible = not data_visible
        window['-KEY-data_col'].update(visible=data_visible)

    if event == 'increment':
        val += 5
        print('val = ', val)
        if val >= 100:
            window['-KEY-fix_prog'].update(visible=False)
            window['-KEY-data_col'].update(visible=True)
        else:
            window['-KEY-fix_prog'].update_bar(val)
        

    if event == "update":
        # update stuff
        window['lat_text'].update(random.uniform(0.0, 1000.0))
        window['long_text'].update(random.uniform(0.0, 1000.0))
        window['hdop_text'].update(random.uniform(0.0, 1.0))
        window['sat_text'].update(random.randrange(0, 30))
        

window.close()
