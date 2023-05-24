#! /usr/bin/python3
import PySimpleGUI as sg
import random
sg.theme("dark grey 9")

has_fix = False
data_visible = False

val = 0

interface_column = [
        [
            sg.Push(),
            sg.Button('increment', visible=True),
            sg.Push(),
        ],
        [
            sg.Push(),
            sg.Button("exit"),
            sg.Push(),
        ],
    ]

data_column = [
        [
            sg.Frame(
                    'Latitude',
                    [[sg.Text(1000.0000, key='lat_text'), sg.Push(), sg.Text('N')]],
                    size=(200, 60),
                    key='lat_frame'
                ),
            sg.Frame(
                    'Longitude',
                    [[sg.Text(1200.0000, key='long_text'), sg.Push(), sg.Text('W')]],
                    size=(200, 60),
                    key='long_frame'
                ),
        ],
        [
            sg.Frame(
                    'EST. ACC.', 
                    [[sg.Text(1000, key='-KEY-acc_est_mm'), sg.Text('mm /'), sg.Text('12', k='-KEY-acc_est_ft'), sg.Text('ft'), sg.Push()]],
                    size=(200, 60)
                ),
            sg.Frame(
                    'HDOP',
                    [[sg.Text(0.69, key='hdop_text'),sg.Push()]],
                    size=(100, 60),
                    key='hdop_frame'
                ),
            sg.Frame(
                    'Satellites',
                    [[sg.Text(12, key='sat_text'),sg.Push()]],
                    size=(100, 60),
                    key='sat_frame'
                ),
            
        ],
        [
            sg.Button('update'),
        ]
    ]

layout = [
        [
            sg.Frame(
                'Data', 
                [[sg.Column(data_column, element_justification='center')]], 
                size=(460, 200),
                k='-KEY-data_col', 
                visible=False,
            ),
            sg.ProgressBar(
                100,
                orientation='horizontal',
                border_width='10',
                key='-KEY-fix_prog',
                visible=True),
        ],
        [
            interface_column
        ]
    ]

# Create the window
window = sg.Window(
        title="ScareCro Provisioner", 
        no_titlebar=True,
        #alpha_channel=0.7,
        layout=layout, size=(480, 320),
        font=('Arial', 11, 'italic')
    )


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "exit" or event == sg.WIN_CLOSED:
        break


    if event == 'increment':
        val += 20
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
        hdop = random.uniform(0.0, 1.0)
        text_color = None
        if hdop > 0.8: 
            text_color = '#fc0505'
        elif hdop <= 0.79 and hdop >= 2:
            text_color = '#fce705'
        else:
            text_color='#08cc18'

        window['hdop_text'].update(hdop, text_color=text_color)
        window['sat_text'].update(random.randrange(0, 30))
        acc_est_mm = random.randrange(300, 3000)
        acc_est_ft = acc_est_mm * 0.00328084
        window['-KEY-acc_est_mm'].update(acc_est_mm)
        window['-KEY-acc_est_ft'].update(acc_est_ft)
        

window.close()
