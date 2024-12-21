import PySimpleGUI as sg
from serial.tools import list_ports
from pydobotplus import Dobot
import sys
import os

def resource_path(relative_path):
    """ Get the absolute path to a resource. Works for development and PyInstaller. """
    try:
        # PyInstaller creates a temporary folder at runtime and stores files there
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


layout = [
    [sg.Image(filename=resource_path("images/red_circle.png"), key='-CHANGE_IMAGE-', subsample=10), sg.Button(button_text='Connect', key='-CONNECT-')],
    [sg.Push(), sg.Button(button_text='Get Position', disabled=True, key='-GET_POS-'), sg.Push()],
    [sg.Text(text = 'X'), sg.Input(readonly=True, key='-X-')],
    [sg.Text(text = 'Y'), sg.Input(readonly=True, key='-Y-')],
    [sg.Text(text = 'Z'), sg.Input(readonly=True, key='-Z-')]
]

window = sg.Window(title='Dobot position', layout=layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == '-CONNECT-':
        button_text = window['-CONNECT-'].ButtonText
        if button_text == 'Connect':
            available_ports = list_ports.comports()
            print(f'available ports: {[x.device for x in available_ports]}')
            port = available_ports[0].device

            device = Dobot(port=port)

            window['-CONNECT-'].update('Disconnect')
            window['-CHANGE_IMAGE-'].update(filename=resource_path("images/green_circle.png"), subsample=10)
            window['-GET_POS-'].update(disabled=False)

        else:
            device.close()
            window['-GET_POS-'].update(disabled=True)
            window['-CONNECT-'].update('Connect')
            window['-CHANGE_IMAGE-'].update(filename=resource_path("images/red_circle.png"), subsample=10)

            window['-X-'].update('')
            window['-Y-'].update('')
            window['-Z-'].update('')

    elif event == '-GET_POS-':
        position = device.get_pose()
        window['-X-'].update(str(position.position.x))
        window['-Y-'].update(str(position.position.y))
        window['-Z-'].update(str(position.position.z))
window.close()