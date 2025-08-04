import json, os, websocket, time, hashlib
import FreeSimpleGUIWeb as sg
from cryptography.fernet import Fernet

# used to encrypt and decrypt thee settings file
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

# allows for the settings file to be read without having to repeat the code
def readSettings():
    with open("settings/settings.json","rb") as f:
        decryptFile("settings/settings.json")
        settings = json.load(f)
    encryptFile("settings/settings.json")
    return settings

# allows for the account information to be saved without having to repeat the code
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

# this changes the saved settings with a GUI
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

# for first time startup, generates the key and settings files
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

# stores all the looping variables
app = True
Connectloop = True
loginloop = True
account = False
savedDetails = True
ws = websocket.WebSocket()

# any saved settings gets stored
settings = readSettings()
username = settings["username"]
password = settings["password"]
server = settings["server"]

while Connectloop == True:
    # checks if there is a saved server and if the user wants to connect to it
    if server != "":
        layout = [[sg.Text("You have a server saved. Do you want to connect to it?")],
                  [sg.Button("Yes"), sg.Button("No")]]
        window = sg.Window("Saved Server", layout)
        event, values = window.read()
        if event == "Yes":
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
            except:
                layout = [  [sg.Text("Could not connect is the server up?")],
                            [sg.Text("retrying in 5 seconds")] ]
                window = sg.Window('Error', layout)
                time.sleep(5)
        elif event == sg.WIN_CLOSED or event == 'No':
            layout = [  [sg.Text("please enter in the ws url")],
                        [sg.Text("example: ws://127.0.0.1:8000")],
                        [sg.InputText()],
                        [sg.Button('Confirm'), sg.Button('Cancel')] ]
            window = sg.Window('Connect to server', layout)
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
    else:
        # if there is no saved server, the user is asked to enter one
        layout = [  [sg.Text("please enter in the ws url")],
                    [sg.Text("example: ws://127.0.0.1:8000")],
                    [sg.InputText()],
                    [sg.Button('Confirm'), sg.Button('Cancel')] ]
        window = sg.Window('Connect to server', layout)
        event, values = window.read()
        window.close()
        if event == "Confirm":
            url = values[0]
            # try loop to see if the server is up
            try:
                layout = [  [sg.Text(f"connecting to {url}")],
                            [sg.Text("Please Wait")]]
                window = sg.Window('Connecting to server', layout)
                ws.connect(url)
                Connectloop = False
                layout = [ [sg.Text("Do you want to save the URL?")],
                            [sg.Button("Yes"), sg.Button("No")]]
                window = sg.Window("Save details?", layout)
                event, values = window.read()
                window.close()
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
                layout = [  [sg.Text("Could not connect is the server up?")],
                            [sg.Text("retrying in 5 seconds")] ]
                window = sg.Window('Error', layout)
                time.sleep(5)

    while app == True:
        # if there are saved details, the user is asked if they want to use them
        while savedDetails == True:
            if settings["username"] != "" and settings["password"] != "":
                layout = [  [sg.Text("account details found do you want to use them?")],
                            [sg.Button('Yes'), sg.Button('No')] ]
                window = sg.Window("login", layout)
                event, values = window.read()
                if event == "Yes":
                    ws.send("login")
                    ws.send(json.dumps({"username":username,"password":password}))
                    response = ws.recv()
                    # if the login is successful, the user is logged in
                    # this is asked by sending a request to the server
                    if response == "success":
                        loginloop = False
                        account = True
                        savedDetails = False
                        break
                    else:
                        layout = [  [sg.Text("invalid username or password")]
                                    [sg.Button('Ok')] ]
                        window = sg.Window("Error", layout)
                        loginloop = True
                else: 
                    loginloop = True
                    savedDetails = False
                    break
            else: 
                loginloop = True
                savedDetails = False
                break
        while loginloop == True:
            # if there are no saved details it will prompt the user to login or register
            layout = [  [sg.Text("please either login or register")],
                        [sg.Button('login'), sg.Button('register')] ]
            window = sg.Window('login', layout)
            event, values = window.read()
            message = event
            if message == "login":
                # creates the GUI for the login
                layout = [  [sg.Text("please enter in your username and password")],
                            [sg.Text("username"),sg.InputText(key='username')],
                            [sg.Text("password "),sg.InputText(key='password')],
                            [sg.Button('Ok'), sg.Button('Cancel')] ]
                window = sg.Window('login', layout)
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                username = values['username']
                password = hashlib.sha256(values['password'].encode()).hexdigest()
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
                    account = True
                else:
                    layout = [  [sg.Text("invalid username or password")],
                                [sg.Text("please enter them again")],
                                [sg.Button('Ok')] ]
                    window = sg.Window("Error", layout)

            elif message == "register":
                # much like the login gui but this one is for registering
                ws.send("register")
                layout = [  [sg.Text("please enter in your username and password")],
                            [sg.Text("username"),sg.InputText(key='username')],
                            [sg.Text("password "),sg.InputText(key='password')],
                            [sg.Button('Ok'), sg.Button('Cancel')] ]
                window = sg.Window('login', layout)
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Cancel':
                    break
                username = values['username']
                password = hashlib.sha256(values['password'].encode()).hexdigest()
                ws.send(json.dumps({"username":username,"password":password}))
                response = ws.recv()
                if response == "created":
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
                exit(0)
        while account == True:
            try:
                # welcomes the user and lists the notes and options for the user
                layout = []
                layout += [[sg.Text(f"Welcome {username}")],
                           [sg.Text("Notes:")]]
                settingsloop = False
                ws.send("getNotes")
                ws.send(json.dumps({"username":username,"password":password}))
                response = ws.recv()
                notes = json.loads(response)
                for note in notes:
                    layout += [[sg.Text(note)]]
                layout += [[sg.Text("What would you like to do?")],
                           [sg.Button("create"),sg.Button("read"),sg.Button("settings"),sg.Button("Exit")]]
                window = sg.Window("Notes", layout)
                event, values = window.read()
                message = event
                if message == "read":
                    # allows the user to read a note by clicking on it
                    layout = [[sg.Text("what note would you like to read")]] + [[sg.Button(note)] for note in notes] + [[sg.Text()],[sg.Button("Exit")]]
                    window = sg.Window("Read Note", layout)
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == "Exit":
                        break
                    else: title = event
                    ws.send("readNote")
                    ws.send(json.dumps({"username":username,"password":password,"title":title}))
                    response = ws.recv()
                    if response != "exists":
                        note = json.loads(response)
                        title = note["title"]
                        layout = [[sg.Text(f"Title: {title}")],
                                  [sg.Text("Content:")],
                                  [sg.Text(note["content"])],
                                  [sg.Text("What would you like to do?")],
                                  [sg.Button("edit"),sg.Button("delete"),sg.Button("go back")]]
                        window = sg.Window("Read Note", layout)
                        event, values = window.read()
                        message = event
                        if message == sg.WIN_CLOSED or message == "go back":
                            break
                        elif message == "edit":
                            # allows the user to edit a note
                            layout = [[sg.Text("what would you like to edit?")],
                                      [sg.Button("title"),sg.Button("content")], [sg.Button("go back")]]
                            window = sg.Window("Edit Note", layout)
                            event, values = window.read()
                            message = event
                            if message == "title":
                                # allows the user to edit the title
                                layout = [[sg.Text("please enter in the new title")],
                                          [sg.InputText(key='title')],
                                          [sg.Button('Ok'), sg.Button('Cancel')]]
                                window = sg.Window('Change title', layout)
                                event, values = window.read()
                                if event == sg.WIN_CLOSED or event == 'Cancel':
                                    break
                                Newtitle = values['title']
                                ws.send("editNote")
                                ws.send(json.dumps({"username":username,"password":password,"title":title,"newContent":note["content"],"newTitle":Newtitle,"conORtitle":"title"}))
                                response = ws.recv()
                                if response == "success":
                                    layout = [[sg.Text("note edited")],
                                              [sg.Button("go back")]]
                                    window = sg.Window("Edit Note", layout)
                                else:
                                    layout = [[sg.Text("an error has occured")],
                                              [sg.Text(f"error: {response}")],
                                              [sg.Button("go back")]]
                                    window = sg.Window("Error", layout)
                            elif message == "content":
                                # allows the user to edit the content
                                layout = [[sg.Text("please enter in the new content")],
                                          [sg.Multiline(size=(None, 3),key='content')],
                                          [sg.Button('Ok'), sg.Button('Cancel')]]
                                window = sg.Window('Change content', layout)
                                event, values = window.read()
                                if event == sg.WIN_CLOSED or event == 'Cancel':
                                    break
                                Newcontent = values['content']
                                ws.send("editNote")
                                ws.send(json.dumps({"username":username,"password":password,"title":title,"newContent":Newcontent,"newTitle":note["title"],"conORtitle":"content"}))
                                response = ws.recv()
                                if response == "success":
                                    layout = [[sg.Text("note edited")],
                                              [sg.Button("go back")]]
                                    window = sg.Window("Edit Note", layout)
                                else:
                                    layout = [[sg.Text("an error has occured")],
                                              [sg.Text(f"error: {response}")],
                                              [sg.Button("go back")]]
                                    window = sg.Window("Error", layout)
                            else:
                                break
                        elif message == "delete":
                            # allows the user to delete a note with a warning
                            layout = [[sg.Text("are you sure you want to delete this note?")],
                                      [sg.Button("yes"),sg.Button("no")]]
                            window = sg.Window("Delete Note", layout)
                            event, values = window.read()
                            message = event
                            if message == "yes":
                                ws.send("deleteNote")
                                ws.send(json.dumps({"username":username,"password":password,"title":title}))
                                response = ws.recv()
                                if response == "success":
                                    layout = [[sg.Text("note Deleted")],
                                              [sg.Button("go back")]]
                                    window = sg.Window("Deleted Note", layout)
                                else:
                                    layout = [[sg.Text("an error has occured")],
                                              [sg.Text(f"error: {response}")],
                                              [sg.Button("go back")]]
                                    window = sg.Window("Error", layout)
                            else: 
                                break
                        elif message == "go back":
                            break
                    else:
                        # if there isnt a note with that title
                        layout = [[sg.Text("an error has occured")],
                                  [sg.Text(f"error: {response}")],
                                  [sg.Button("go back")]]
                        window = sg.Window("Error", layout)
                elif message == "create":
                    # allows the user to create a note
                    layout = [  [sg.Text("please enter in the title")],
                                [sg.InputText(key='title')],
                                [sg.Text("please enter in the new content")],
                                [sg.Multiline(size=(50, 3),key='content')],
                                [sg.Button('Ok'), sg.Button('Cancel')]]
                    window = sg.Window('Create Note', layout)
                    event, values = window.read()
                    if event == sg.WIN_CLOSED or event == 'Cancel':
                        break
                    title = values['title']
                    content = values['content']
                    ws.send("createNote")
                    ws.send(json.dumps({"username":username,"password":password,"title":title,"content":content}))
                    response = ws.recv()
                    if response == "success":
                        layout = [[sg.Text("note created")],
                                  [sg.Button("go back")]]
                        window = sg.Window("Edit Note", layout)
                    else:
                        layout = [[sg.Text("an error has occured")],
                                  [sg.Text(f"error: {response}")],
                                  [sg.Button("go back")]]
                        window = sg.Window("Error", layout)
                elif message == "Exit" or message == sg.WIN_CLOSED:
                    account = False
                    exit(0)
                elif message == "settings":
                    # allows the user to change their settings
                    settingsloop = True
                    while settingsloop == True:
                        layout = [  [sg.Text("what would you like to change")],
                                    [sg.Button("change username"),sg.Button("change password"),sg.Button("change server"),sg.Button("go back")]]
                        window = sg.Window("Settings", layout)
                        event, values = window.read()
                        message = event
                        if message == "change username":
                            settings = changeSettings("username")
                            username = settings["username"]
                        elif message == "change password":
                            settings = changeSettings("password")
                            password = settings["password"]
                        elif message == "change server":
                            settings = changeSettings("server")
                            server = settings["server"]
                        elif message == sg.WIN_CLOSED or message == "go back":
                            settingsloop = False
                            break
                        else:
                            print("invalid message")
                            print("please try again")
                else:
                    print("invalid message")
            except Exception as e:
                # if the connection is lost the program will attempt to reconnect
                if str(e) == "[Errno 32] Broken pipe":
                    print("\nDisconnected attempting to reconnect\n")
                    ws.connect(url)
                else:
                    # if that isnt the error then it will give out the error
                    print("an error has occured")
                    print(f"error: {e}")
                    exit(0)
        