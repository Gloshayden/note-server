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
loginloop = True
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
        elif event == sg.WIN_CLOSED or event == 'No':
            window.close()
            layout = [  [sg.Text("please enter in the ws url")],
                        [sg.Text("example: ws://127.0.0.1:8000")],
                        [sg.InputText()],
                        [sg.Button('Confirm'), sg.Button('Cancel')] ]
            window = sg.Window('Connect to server', layout)
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
    event, values = window.read()
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
        if settings["username"] != "" and settings["password"] != "":
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
                    window.close()
                    break
                else:
                    window.close()
                    layout = [  [sg.Text("invalid username or password")]
                                [sg.Button('Ok')] ]
                    window = sg.Window("Error", layout)
                    loginloop = True
            else: loginloop = True
        else: loginloop = True
        while loginloop == True:
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
                ws.send("login")
                ws.send(json.dumps({"username":username,"password":password}))
                response = ws.recv()
                if response == "success":
                    window.close()
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
                            [sg.Text("username"),sg.InputText(key='username')],
                            [sg.Text("password "),sg.InputText(key='password')],
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
                        loginloop = False
                        account = True
                        username, password = saveAccount(username, password)
                    elif event == "No":
                        loginloop = False
                        account = True
                        break
                if response == "exists":
                    window.close()
                    layout = [  [sg.Text("an account wihth that username already exists")],
                                [sg.Text("please try again")],
                                [sg.Button('Ok')] ]
                    window = sg.Window("Error", layout)
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == 'Cancel':
                        break
                else:
                    print("unknown error")
                    print("please try again\n")
            else:
                print("invalid message")
            while account == True:
                try:
                    window.close()
                    layout = []
                    layout += [[sg.Text(f"Welcome {username}")]]
                    layout += [[sg.Text("Notes:")]]
                    settingsloop = False
                    ws.send("getNotes")
                    ws.send(json.dumps({"username":username,"password":password}))
                    response = ws.recv()
                    notes = json.loads(response)
                    for note in notes:
                        layout += [[sg.Text(note)]]
                    layout += [[sg.Text("What would you like to do?")]]
                    layout += [[sg.Button("create"),sg.Button("read"),sg.Button("settings"),sg.Button("Exit")]]
                    window = sg.Window("Notes", layout)
                    event, values = window.read()
                    message = event
                    if message == "read":
                        print("please enter in the title of the note")
                        title = input()
                        ws.send("readNote")
                        ws.send(json.dumps({"username":username,"password":password,"title":title}))
                        response = ws.recv()
                        if response != "exists":
                            note = json.loads(response)
                            title = note["title"]
                            print(f"\nTitle:{note["title"]} \n{note['content']}\n")
                            print("what would you like to do?")
                            print("edit, delete or (go) back")
                            message = input()
                            if message == "edit":
                                print("would you like to edit the title or the content?")
                                message = input()
                                if message == "title":
                                    print("please enter in the new title")
                                    Newtitle = input()
                                    ws.send("editNote")
                                    ws.send(json.dumps({"username":username,"password":password,"title":title,"Newcontent":note["content"],"Newtitle":Newtitle,"conORtitle":"title"}))
                                    response = ws.recv()
                                    if response == "success":
                                        print("note edited")
                                    else:
                                        print("an error has occured")
                                        print(f"error: {response}")
                                elif message == "content":
                                    print("please enter in the new content")
                                    Newcontent = input()
                                    ws.send("editNote")
                                    ws.send(json.dumps({"username":username,"password":password,"title":title,"Newcontent":Newcontent,"Newtitle":note["title"],"conORtitle":"content"}))
                                    response = ws.recv()
                                    if response == "success":
                                        print("note edited")
                                    else:
                                        print("an error has occured")
                                        print(f"error: {response}")
                                else:
                                    print("invalid message")
                            elif message == "delete":
                                ws.send("deleteNote")
                                ws.send(json.dumps({"username":username,"password":password,"title":title}))
                                response = ws.recv()
                                if response == "success":
                                    print("note deleted")
                                else:
                                    print("an error has occured")
                                    print(f"error: {response}")
    
                            elif message == "back":
                                continue
                            else:
                                print("invalid message")
                                print("please try again")
                        else:
                            print("note not found")
                            print("please try again")
                    elif message == "add":
                        print("please enter in the title of the note")
                        title = input()
                        print("please enter in the content of the note")
                        content = input()
                        ws.send("createNote")
                        ws.send(json.dumps({"username":username,"password":password,"title":title,"content":content}))
                        response = ws.recv()
                        if response == "success":
                            print("note created")
                        else:
                            print("an error has occured")
                            print(f"error: {response}")
                    elif message == "Exit" or message == sg.WIN_CLOSED:
                        window.close()
                        account = False
                        exit(0)
                    elif message == "settings":
                        settingsloop = True
                        while settingsloop == True:
                            print("What would you like to do?")
                            print("change username, change password, change server or (go) back")
                            message = input()
                            if message == "change username":
                                settings = changeSettings("username")
                                username = settings["username"]
                            elif message == "change password":
                                settings = changeSettings("password")
                                password = settings["password"]
                            elif message == "change server":
                                settings = changeSettings("server")
                                server = settings["server"]
                            elif message == "go" or message == "back":
                                settingsloop = False
                            else:
                                print("invalid message")
                                print("please try again")
                    else:
                        print("invalid message")
                except Exception as e:
                    if str(e) == "[Errno 32] Broken pipe":
                        print("\nDisconnected attempting to reconnect\n")
                        ws.connect(url)
                    else:
                        print("an error has occured")
                        print(f"error: {e}")
                        exit(0)
            