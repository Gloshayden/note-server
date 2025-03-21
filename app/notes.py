import json, os, websocket

app = True
Connectloop = True
account = False
ws = websocket.WebSocket()

print("Hi there welcome to the notes app!")
print ("please enter in the ws url")
print("example: ws://127.0.0.1:8000")
while Connectloop == True:
    url = input()
    try:
        ws.connect(url)
        Connectloop = False
    except:
        print("invalid url")
        Connectloop = True

while app == True:
    loginloop = True
    while loginloop == True:
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
                loginloop = False
                print("account created")
                account = True
            elif response == "exists":
                print("account already exists")
                print("please try again")
                print("")
            else:
                print("unknown error")
                print("please try again")
                print("")
        else:
            print("invalid message")
    while account == True:
        print(f"\nwelcome {username}\n")
        ws.send("getNotes")
        ws.send(json.dumps({"username":username,"password":password}))
        response = ws.recv()
        notes = json.loads(response)
        for note in notes:
            print(note)
        print("\nWhat would you like to do?")
        print("read or add (a note)")
        message = input()
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
        else:
            print("invalid message")