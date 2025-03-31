import json, os, websocket, time
import FreeSimpleGUI as sg
from cryptography.fernet import Fernet

def encryptFile(FileName):
    with open(FileName,"rb") as f:
        Original = f.read()
    encoded_file = cipher_suite.encrypt(Original)
    with open(FileName,"wb") as f:
        f.write(encoded_file)
    return encoded_file

def decryptFile(FileName):
    with open(FileName,"rb") as f:
        Encrypted = f.read()
    decoded_file = cipher_suite.decrypt(Encrypted)
    with open(FileName,"wb") as f:
        f.write(decoded_file)
    return decoded_file

def readSettings():
    with open("settings/settings.json","rb") as f:
        decryptFile("settings/settings.json")
        settings = json.load(f)
    encryptFile("settings/settings.json")
    return settings

def saveAccount(username, password):
    print("Do you want to save the account details? (y/n)")
    message = input().lower()
    if message == "y":
        decryptFile("settings/settings.json")
        settings = {"username":username,"password":password,"server":server}
        with open("settings/settings.json","w") as f:
            json.dump(settings,f)
        encryptFile("settings/settings.json")
        settings = readSettings()
        username = settings["username"]
        password = settings["password"]
        return username, password
    else:
        print("account details not saved")

def changeSettings(choice):
    print("what would you like to do?")
    print("delete (setting) or change (setting)")
    message = input().lower()
    if message == "delete":
        decryptFile("settings/settings.json")
        if choice == "server": message = {"username":username,"password":password,"server":""}
        elif choice == "username": message = {"username":"","password":password,"server":server}
        elif choice == "password": message = {"username":username,"password":"","server":server}
        with open("settings/settings.json","w") as f:
            json.dump(message,f)
        encryptFile("settings/settings.json")
        settings = readSettings()
        return settings
    elif message == "change":
        decryptFile("settings/settings.json")
        if choice == "server": message = {"username":username,"password":password,"server":input()}
        elif choice == "username": message = {"username":input(),"password":password,"server":server}
        elif choice == "password": message = {"username":username,"password":input(),"server":server}
        with open("settings/settings.json","w") as f:
            json.dump(message,f)
        encryptFile("settings/settings.json")
        settings = readSettings()
        return settings

if not os.path.exists("settings"):
    os.mkdir("settings")
    key = Fernet.generate_key()
    with open("settings/key.key","wb") as f:
        f.write(key)
    cipher_suite = Fernet(key)
    settings = {"username":"","password":"","server":""}
    with open("settings/settings.json","w") as f:
        json.dump(settings,f)
    encryptFile("settings/settings.json")
with open("settings/key.key","rb") as f:
    keyinfo = f.read()
cipher_suite = Fernet(keyinfo)

app = True
Connectloop = True
account = False
ws = websocket.WebSocket()

settings = readSettings()
username = settings["username"]
password = settings["password"]
server = settings["server"]

layout = [  [sg.Text("please enter in the ws url")],
            [sg.Text("example: ws://127.0.0.1:8000")],
            [sg.InputText()],
            [sg.Button('Confirm'), sg.Button('Cancel')] ]

window = sg.Window('Connect to server', layout)
while Connectloop == True:
    if server != "":
        window.close()
        url = server
        layout = [  [sg.Text(f"connecting to {url}")],
                    [sg.Text("Please Wait")]]
        window = sg.Window('Connecting to server', layout)
        try:
            layout = [  [sg.Text(f"connecting to {url}")],
                        [sg.Text("Please Wait")]]
            window = sg.Window('Connecting to server', layout)
            ws.connect(url)
            Connectloop = False
            window.close()
        except:
            window.close()
            layout = [  [sg.Text("Could not connect is the server up?")],
                        [sg.Text("retrying in 5 seconds")] ]
            window = sg.Window('Error', layout)
            time.sleep(5)
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == "Confirm":
        window.close()
        url = values[0]
        try:
            layout = [  [sg.Text(f"connecting to {url}")],
                        [sg.Text("Please Wait")]]
            window = sg.Window('Connecting to server', layout)
            ws.connect(url)
            Connectloop = False
            window.close()
        except:
            window.close()
            layout = [  [sg.Text("Could not connect is the server up?")],
                        [sg.Text("retrying in 5 seconds")] ]
            window = sg.Window('Error', layout)
            time.sleep(5)