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
        decryptFile("settings/settings.json")
        settings = {"username":username,"password":password,"server":server}
        with open("settings/settings.json","w") as f:
            json.dump(settings,f)
        encryptFile("settings/settings.json")
        settings = readSettings()
        username = settings["username"]
        password = settings["password"]
        return username, password

def changeSettings(choice):
    layout = [ [sg.Text("Do you want to delete or change a setting?")],
                [sg.Button("Delete"), sg.Button("Change"), sg.Button("Back")]]
    window = sg.Window("Change settings", layout)
    event, values = window.read()
    message = event
    if message == "Delete":
        decryptFile("settings/settings.json")
        if choice == "server": message = {"username":username,"password":password,"server":""}
        elif choice == "username": message = {"username":"","password":password,"server":server}
        elif choice == "password": message = {"username":username,"password":"","server":server}
        with open("settings/settings.json","w") as f:
            json.dump(message,f)
        encryptFile("settings/settings.json")
        settings = readSettings()
        return settings
    elif message == "Change":
        window.close()
        layout = [  [sg.Text("What would you like to replace it with")],
                    [sg.Text("New Info"),sg.InputText(key='info')],
                    [sg.Button('Ok'), sg.Button('Cancel')] ]
        window = sg.Window("Change settings", layout)
        event, values = window.Read()
        newSetting = values['info']
        decryptFile("settings/settings.json")
        if choice == "server": message = {"username":username,"password":password,"server":newSetting}
        elif choice == "username": message = {"username":newSetting,"password":password,"server":server}
        elif choice == "password": message = {"username":username,"password":newSetting,"server":server}
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
        layout = [[sg.Text("You have a server saved. Do you want to connect to it?")],
                  [sg.Button("Yes"), sg.Button("No")]]
        window = sg.Window("Saved Server", layout)
        event, values = window.read()
        if event == "Yes":
            window.close()
            url = server
            print("TEst2")
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
    if event == sg.WIN_CLOSED or event == 'No':
        window.close()
        print("Test")
        layout = [  [sg.Text("please enter in the ws url")],
                    [sg.Text("example: ws://127.0.0.1:8000")],
                    [sg.InputText()],
                    [sg.Button('Confirm'), sg.Button('Cancel')] ]
        window = sg.Window('Connect to server', layout)
        event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == "Confirm":
        window.close()
        url = values[0]
        try:
            layout = [  [sg.Text(f"connecting to {url}")],
                        [sg.Text("Please Wait")]]
            window = sg.Window('Connecting to server', layout)
            ws.connect(url)
            Connectloop = False
            window.close()
            layout = [ [sg.Text("Do you want to save the URL?")],
                        [sg.Button("Yes"), sg.Button("No")]]
            window = sg.Window("Save details?", layout)
            event, values = window.read()
            if event == "Yes":
                decryptFile("settings/settings.json")
                settings = {"username":username,"password":password,"server":url}
                with open("settings/settings.json","w") as f:
                    json.dump(settings,f)
                encryptFile("settings/settings.json")
                settings = readSettings()
                server = settings["server"]
                Connectloop = False
        except:
            window.close()
            layout = [  [sg.Text("Could not connect is the server up?")],
                        [sg.Text("retrying in 5 seconds")] ]
            window = sg.Window('Error', layout)
            time.sleep(5)

    while app == True:
        while loginloop == True:
            if username != "" and password != "":
                layout = [  [sg.Text("account details found do you want to use them?")],
                            [sg.Button('Yes'), sg.Button('No')] ]
                window = sg.Window("login", layout)
                event, values = window.read()
                if event == "Yes":
                    ws.send("login")
                    ws.send(json.dumps({"username":username,"password":password}))
                    response = ws.recv()
                    if response == "success":
                        loginloop = False
                        account = True
                    else:
                        window.close()
                        layout = [  [sg.Text("invalid username or password")],
                                    [sg.Text("please enter them again")],
                                    [sg.Button('Ok')] ]
                        window = sg.Window("Error", layout)
                        loginloop = True
                else: loginloop = True
            else: loginloop = True
            window.close()
            layout = [  [sg.Text("please either login or register")],
                        [sg.Button('login'), sg.Button('register')] ]
            window = sg.Window('login', layout)
            event, values = window.read()
            message = event
            if message == "login":
                window.close()
                layout = [  [sg.Text("please enter in your username and password")],
                            [sg.Text("username"),sg.InputText(key='username')],
                            [sg.Text("password "),sg.InputText(key='password')],
                            [sg.Button('Ok'), sg.Button('Cancel')] ]
                window = sg.Window('login', layout)
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                username = values['username']
                password = values['password']
                print(f"{username} {password}")
                ws.send("login")
                ws.send(json.dumps({"username":username,"password":password}))
                response = ws.recv()
                if response == "success":
                    loginloop = False
                    layout = [  [sg.Text("Do you want to save your account details?")],
                                [sg.Button('Yes'), sg.Button('No')] ]
                    window = sg.Window("Save Details?", layout)
                    event, values = window.read()
                    if event == "Yes":
                        username, password = saveAccount(username, password)
                        window.close()
                    if event == "No":
                        window.close()
                    account = True
                else:
                    window.close()
                    layout = [  [sg.Text("invalid username or password")],
                                [sg.Text("please enter them again")],
                                [sg.Button('Ok')] ]
                    window = sg.Window("Error", layout)

            elif message == "register":
                ws.send("register")
                window.close()
                layout = [  [sg.Text("please enter in your username and password")],
                            [sg.InputText(default_text='Username', key='username')],
                            [sg.InputText(default_text='Password', key='password')],
                            [sg.Button('Ok'), sg.Button('Cancel')] ]
                window = sg.Window('login', layout)
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                username = values['username']
                password = values['password']
                ws.send(json.dumps({"username":username,"password":password}))
                response = ws.recv()
                if response == "created":
                    window.close()
                    layout = [  [sg.Text("Do you want to save your account details?")],
                                [sg.Button('Yes'), sg.Button('No')] ]
                    window = sg.Window("Save Details?", layout)
                    event, values = window.read()
                    if event == "Yes":
                        username, password = saveAccount(username, password)
                    elif event == "No":
                        break
                    loginloop = False
                    account = True
                elif response == "exists":
                    layout = [  [sg.Text("an account wihth that username already exists")],
                                [sg.Text("please try again")],
                                [sg.Button('Ok')] ]
                    window = sg.Window("Error", layout)
                elif event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                else:
                    print("unknown error")
                    print("please try again\n")
            else:
                app = False
                loginloop = False