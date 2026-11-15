import serial
import time
#import keyboard
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
import serial.tools.list_ports
from datetime import datetime
import os
import sys

def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу (работает и для dev-режима, и для PyInstaller)"""
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
session = PromptSession(history=FileHistory('.my_cli_history'))
print("--- Arduino-cli Monitoring ---")
commands = ("connect", "show ports", "disconnect", "start parsing", "write", "exit", "help", "ft", "rf")
separator = '>'
flag = False
while True:
    # cmd = session.prompt("arduino-cli ~$")
    cmd = input("arduino-cli ~$")
    one = cmd.split(separator)
    if cmd == commands[1]:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            print(port.device, "\t", port.description)
    elif one[0] == commands[0]:
        ser = serial.Serial(one[1], 9600, timeout=1)
        flag = False
        print("Connecting succsess")
    elif cmd == commands[2]:
        ser.close()
        flag = True
        print("Port closed succsess!")
    elif one[0] == commands[3]:
        for i in range(0, int(one[1])):
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                print(line)
                # time.sleep(0.05)
    elif one[0] == commands[4]:
        str = one[1]
        ser.write(str.encode('utf-8'))
    elif cmd == commands[5]:
        if flag == False:
            ser.close()
        break
    elif cmd == commands[6]:
        path = resource_path("help.txt")
        with open("path", "r") as file:
            print(file.read())
    elif one[0] == commands[8]:
        duration = int(one[1])
        start_time = time.time()
        data = datetime.now()
        while time.time() - start_time < duration:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                with open(f"weather_log_{data}.txt", "a") as file:
                    file.write(line + "\n")
