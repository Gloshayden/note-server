import json, os, websocket, time
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

# this changes the saved settings with a CLI
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
account = False
ws = websocket.WebSocket()

settings = readSettings()
username = settings["username"]
password = settings["password"]
server = settings["server"]

print("Hi there welcome to the notes app!")
print("please enter in the ws url")
print("example: ws://127.0.0.1:8000")
while Connectloop == True:
    # checks if there is a saved server and if the user wants to connect to it
    if server != "":
        url = server
        print(f"connecting to {url}")
        try:
            ws.connect(url)
            Connectloop = False
        except:
            print("Could not connect is the server up?")
            print("retrying in 5 seconds")
            time.sleep(5)
    else:
        # if there is no saved server, the user is asked to enter one
        url = input()
    try:
        # try loop to see if the server is up
        ws.connect(url)
        if server == "":
            print("Do you want to save the server URL? (y/n)")
            message = input().lower()
            if message == "y":
                decryptFile("settings/settings.json")
                settings = {"username":username,"password":password,"server":url}
                with open("settings/settings.json","w") as f:
                    json.dump(settings,f)
                encryptFile("settings/settings.json")
                settings = readSettings()
                server = settings["server"]
                Connectloop = False
            else:
                print("server url not saved")
                Connectloop = False
    except:
        print("invalid url is the server up?")
        Connectloop = True

    while app == True:
        # if there are saved details, the user is asked if they want to use them
        if username != "" and password != "":
            print("account details found do you want to use them? (y/n)")
            message = input().lower()
            if message == "y":
                ws.send("login")
                ws.send(json.dumps({"username":username,"password":password}))
                response = ws.recv()
                # if the login is successful, the user is logged in
                # this is asked by sending a request to the server
                if response == "success":
                    print("successfully logged in")
                    loginloop = False
                    account = True
                else:
                    print("invalid username or password")
                    print("please enter them again\n")
                    loginloop = True
            else: loginloop = True
        else: loginloop = True
        while loginloop == True:
            if username != "" and password != "":
                print("account details found do you want to use them? (y/n)")
                message = input().lower()
                if message == "y":
                    ws.send("login")
                    ws.send(json.dumps({"username":username,"password":password}))
                    response = ws.recv()
                    if response == "success":
                        print("successfully logged in")
                        loginloop = False
                        account = True
                    else:
                        print("invalid username or password")
                        print("please enter them again\n")
                        loginloop = True
                else: loginloop = True
            else: loginloop = True
            # if there are no saved details it will prompt the user to login or register
            print("please either login or register")
            message = input()
            if message == "login":
                ws.send("login")
                print("please enter in your username")
                username = input()
                print("please enter in your password")
                password = input()
                ws.send(json.dumps({"username":username,"password":password}))
                response = ws.recv()
                if response == "success":
                    loginloop = False
                    print("successfully logged in")
                    username, password = saveAccount(username, password)
                    account = True

            elif message == "register":
                ws.send("register")
                print("please enter in your username")
                username = input()
                print("please enter in your password")
                password = input()
                ws.send(json.dumps({"username":username,"password":password}))
                response = ws.recv()
                if response == "created":
                    username, password = saveAccount(username, password)
                    loginloop = False
                    account = True
                elif response == "Exists":
                    print("account already exists")
                    print("please try again\n")
                else:
                    print("unknown error")
                    print("please try again\n")
            else:
                print("invalid message")
        while account == True:
            try:
                # welcomes the user and lists the notes and options for the user
                settingsloop = False
                print(f"\nwelcome {username}\n")
                ws.send("getNotes")
                ws.send(json.dumps({"username":username,"password":password}))
                response = ws.recv()
                notes = json.loads(response)
                for note in notes:
                    print(note)
                print("\nWhat would you like to do?")
                print("read, add (a note) or settings")
                message = input()
                if message == "read":
                    # allows the user to read a note by typing out the name
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
                            # allows the user to edit a note
                            print("would you like to edit the title or the content?")
                            message = input()
                            if message == "title":
                                # allows the user to edit the title
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
                                # allows the user to edit the content
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
                            # allows the user to delete a note without a warning
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
                        # if there isnt a note with that title
                        print("note not found")
                        print("please try again")
                elif message == "add":
                    # allows the user to create a note
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
                elif message == "settings":
                    # allows the user to change their settings
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
                # if the connection is lost the program will attempt to reconnect
                if str(e) == "[Errno 32] Broken pipe":
                    print("\nDisconnected attempting to reconnect\n")
                    ws.connect(url)
                else:
                    # if that isnt the error then it will give out the error
                    print("an error has occured")
                    print(f"error: {e}")
                    exit(0)