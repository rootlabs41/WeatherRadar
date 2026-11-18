import serial
import time
#import keyboard
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
import serial.tools.list_ports
from datetime import datetime
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.progress import track
import os
import sys
from threading import Thread
from pathlib import Path
custom_theme = Theme({"info": "bold blue", "warning": "bold yellow", "error": "bold red", "text": "blue", "success": "green bold"})
console = Console(theme=custom_theme)
def resource_path(relative_path):
    try:
        # PyInstaller создает временную папку и хранит путь в _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
session = PromptSession(history=FileHistory('.my_cli_history'))
# console.print("--- Arduino-cli Monitoring ---", style="info")
console.rule("[bold green]Arduino-cli[/] [bold cyan]Monitoring")
commands = ("connect", "show ports", "disconnect", "start parsing", "write", "exit", "help", "ft", "rf", "cbp")
separator = '>'
flag = False
basic_port = None
table = Table(title="Ports")
table.add_column("Port", justify="right", style="bold blue", no_wrap=True)
table.add_column("Description", style="magenta")
duration = 0
ser = None
isConnected = False
def writing():
    global duration
    duration = int(one[1])
    start_time = time.time()
    data = datetime.now()
    while time.time() - start_time < duration:
        if ser.in_waiting > 0 and isConnected:
            line = ser.readline().decode('utf-8').rstrip()
            with open(f"weather_log_{data}.csv", "a") as file:
                file.write(line + "\n")

def loading():
    for i in track(range(duration), description="Processing..."):
        time.sleep(1)
def select_basic_port():
    file = Path("data.json")
    if file.is_file() and file.stat().st_size > 0:
        with open("data.json", "r") as f:
            # global basic_port
            basic_port = f.readline()
    elif not file.is_file() or file.stat().st_size == 0:
        # global basic_port
        port = console.input("[bold green]Select basic port (once): [/]")
        with open("data.json", "w") as f:
            f.write(port)
        basic_port = port

while True:
    # cmd = session.prompt("arduino-cli ~$")
    select_basic_port()
    cmd = console.input("[cyan bold]arduino-cli[/] [green]~$ ")
    one = cmd.split(separator)
    if cmd == commands[1]:
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # console.print(port.device, "\t", port.description, style="text")
            table.add_row(port.device, port.description)
        console.print(table)
    elif one[0] == commands[0]:
        ser = serial.Serial(one[1], 9600, timeout=1)
        flag = False
        isConnected = True
        console.print("Connecting success", style="success")
    elif cmd == commands[2]:
        try:
            ser.close()
            flag = True
            console.print("Port closed success!", style="success")
        except:
            console.print("Arduino isn't connected", style="error")
    elif one[0] == commands[3]:
        for i in range(0, int(one[1])):
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                console.print(line, style="text")
                # time.sleep(0.05)
    elif one[0] == commands[4]:
        str = one[1]
        ser.write(str.encode('utf-8'))
    elif cmd == commands[5]:
        try:
            if flag == False:
                ser.close()
        except:
            console.print("Arduino isn't connected! Skipping closing port", style="warning")
        break
    elif cmd == commands[6]:
        path = resource_path("help.txt")
        with open("help.txt", "r") as file:
            console.print(file.read(), style="text")
    elif one[0] == commands[8]:
        t1 =Thread(target=loading)
        t2 = Thread(target=writing)
        t2.start()
        t1.start()
        t1.join()
        t2.join()
    elif cmd == commands[9]:
        try:
            ser = serial.Serial(port=basic_port, baudrate=9600, timeout=1)
            console.print("Connect sucsess", style="success")
        except:
            console.print("Error connecting to serial port", style="error")
            console.print("Connect arduino", style="error")
