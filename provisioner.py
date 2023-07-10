#! /usr/bin/python3
# generic imports
import PySimpleGUI as sg
import random

import time
# RPi imports
from ublox_gps import UbloxGps
import serial

#sg.theme("dark grey 9")
#sg.theme("dark black")
sg.theme("default 1")

has_fix = False
data_visible = False

val = 0

interface_column = [
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
                    [
                        [
                            sg.Text(1000, key='-KEY-acc_est_mm'), 
                            sg.Text('mm'), 
                            sg.Push()
                        ],
                        [
                            sg.Text('12', key='-KEY-acc_est_ft'), 
                            sg.Text('ft'), 
                            sg.Push()
                        ]
                    ],
                    size=(200, 70),
                    title_location='w',
                    #background_color='#001b96'
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
            sg.Frame(
                'buttons', 
                layout=[
                    [
                        sg.Button('freeze', visible=True),
                        sg.Button('average', visible=True),
                    ]
                ],
                visible=True,
                key='-KEY-gps_buttons'
            ),
            sg.ProgressBar(
                    100,
                    size=(100, 10),
                    pad=20,
                    visible=False,
                    key='-KEY-average_bar',
                )
        ]
    ]

layout = [
        [
            sg.Column(
                   layout=[[sg.Frame(
                        'Fix Status',
                        layout=[[sg.Text('no fix')]],
                        size=(100, 50),
                    )]],
                   justification='center',
                   key='-KEY-fix_status',
                )
        ],
        [
            sg.Frame(
                'Data', 
                [[sg.Column(data_column, element_justification='center')]], 
                size=(460, 250),
                k='-KEY-data_col', 
                visible=False,
            ),
            sg.ProgressBar(
                100,
                size=(100, 10),
                pad=50,
                orientation='horizontal',
                key='-KEY-fix_prog',
                visible=True),
        ],
        [
            interface_column,
        ]
    ]

# Create the window
window = sg.Window(
        title="ScareCro Provisioner", 
        no_titlebar=True,
        #alpha_channel=0.7,
        layout=layout, size=(480, 320),
        font=('Arial', 15, 'bold')
    )


port = serial.Serial('/dev/serial0', baudrate=38400, timeout=1)
gps = UbloxGps(port)


def update_gps():
    print("listening for message")
    try:
        gps_msg = gps.stream_nmea()
        if(gps_msg[1:6] == "GNGGA"):
            msg_parts = gps_msg.split(',')
           
            # number of satellites
            sats = msg_parts[7]

            # set hdop and text color
            hdop = msg_parts[8]
            text_color = None
            if hdop > 0.8: 
                text_color = '#fc0505'
            elif hdop <= 0.79 and hdop >= 2:
                text_color = '#fce705'
            else:
                text_color='#08cc18'

            lat = msg_parts[2]
            lat_hemi = msg_parts[3]
            long = msg_parts[4]
            long_hemi = msg_parts[5]

            # post values to display
            window['hdop_text'].update(hdop, text_color=text_color)
            window['sat_text'].update(sats)
            window['lat_text'].update(lat)
            window['long_text'].update(long)
            

    except (ValueError, IOError) as err:
        print(err)

def cleanup_gps():
    port.close()


def op_with_fix(event, values):
    # End program if user closes window or
    # presses the OK button
    if event == "exit" or event == sg.WIN_CLOSED:
        return False
        

    if event == "freeze":
        # update stuff
        update_gps()
        acc_est_mm = random.randrange(300, 3000)
        acc_est_ft = acc_est_mm * 0.00328084
        window['-KEY-acc_est_mm'].update(acc_est_mm)
        window['-KEY-acc_est_ft'].update(acc_est_ft)

    if event == 'average':
        print('averaging')
        #window['-KEY-update_button'].update(visible=False)
        #window['-KEY-avg_button'].update(visible=False)
        window['-KEY-average_bar'].update(visible=True)
        window['-KEY-gps_buttons'].update(visible=False)
        window['-KEY-average_bar'].update_bar(0)


    return True


ft_t0 = time.perf_counter()
ft_current = ft_t0
ft_timer_timeout = 40

# Create an event loop
while True:
    # use timeout so that we can use timers
    event, values = window.read(timeout=1)

    if has_fix:
        cont = op_with_fix(event, values)
        # update gps values
        update_gps()
        if not cont: break

    else:
        # initiate 40 sec count down on bar
        # show status too?
        if ft_current - ft_t0 <= 40:
            # show percentage of time elapsed
            perc_elapsed = ((ft_current - ft_t0)/40)*100
            print(perc_elapsed)
            window['-KEY-fix_prog'].update_bar(perc_elapsed)
            ft_current = time.perf_counter()

        else:
            has_fix = True
            # transition to GPS data
            window['-KEY-fix_prog'].update_bar(0)
            window['-KEY-fix_prog'].update(visible=False)
            window['-KEY-data_col'].update(visible=True)

            window['-KEY-average_bar'].update(visible=False)
            window['-KEY-gps_buttons'].update(visible=True)
            window['-KEY-fix_status'].update(visible=False)
            window['-KEY-fix_status'].Widget.master.pack_forget()

    if event == "exit" or event == sg.WIN_CLOSED:
        break 

window.close()
