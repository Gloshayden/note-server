import asyncio, os, traceback, sys, app, json
from websockets.server import serve
from datetime import datetime
from cryptography.fernet import Fernet
sys.dont_write_bytecode = True


if not os.path.exists("logs"): os.mkdir("logs")
if not os.path.exists("accounts"): os.mkdir("accounts")
if not os.path.exists("notes"): os.mkdir("notes")
if not os.path.exists("key.key"):
    key = Fernet.generate_key()
    with open("key.key","wb") as f:
        f.write(key)

import encryption
async def handler(websocket):
    try:
        async for message in websocket:
            if message == "close": #closing websocket
                await websocket.send("goodbye")
                return
            elif message == "register": #logging in
                message = json.loads(await websocket.recv())
                username = message["username"] 
                password = message["password"]

                register = app.register(username, password)
                if register == "Created": #account created
                    await websocket.send("created")
                    print(f"account {username} created")
                elif register == "Exists": #account already exists
                    await websocket.send("exists")
                    print(f"{username} tried making an account that already exists")
                else: #unknown error
                    await websocket.send("err")
                

            elif message == "login": #logging in
                message = json.loads(await websocket.recv())
                username = message["username"] 
                password = message["password"]

                login = app.login(username, password)
                if login == "success": #logged in
                    await websocket.send("success")
                    print(f"account {username} logged in")
                elif login == "incorrect": #incorrect details
                    await websocket.send("incorrect")
                    print(f"{username} tried logging in with incorrect password")
                else: #unknown error
                    await websocket.send("err")
                

            elif message == "createNote": #creating a note
                message = json.loads(await websocket.recv())
                username = message["username"] 
                password = message["password"]
                title = message["title"]
                content = message["content"]

                success = app.createNote(username, password, title, content)
                if success == "success": #created note
                    await websocket.send("success")
                    print(f"account {username} created note {title}")
                elif success == "failed": #incorrect details
                    await websocket.send("failed")
                    print(f"{username} tried creating a note with incorrect password")
                elif success == "exists": #note already exists
                    await websocket.send("exists")
                    print(f"{username} tried creating a note that already exists")
                else: #unknown error
                    await websocket.send("err")
            

            elif message == "readNote": #reading a note
                message = json.loads(await websocket.recv())
                username = message["username"] 
                password = message["password"]
                title = message["title"]

                success, notecontent = app.readNote(username, password, title)
                if success == "success": #read success
                    await websocket.send("success")
                    print(f"account {username} read note {title}")
                    await websocket.send(json.dumps(notecontent))
                elif success == "exists": #note doest not exist
                    await websocket.send("exists")
                    print(f"{username} tried reading a note that doesn't exist")
                elif success == "failed": #incorrect details
                    await websocket.send("failed")
                    print(f"{username} tried reading note: {title} with incorrect password")
                else: #unknown error
                    await websocket.send("err")
                    
            elif message == "deleteNote": #deleting a note
                message = json.loads(await websocket.recv())
                username = message["username"] 
                password = message["password"]
                title = message["title"]

                success = app.deleteNote(username, password, title)
                if success == "success": #delete success
                    await websocket.send("success")
                    print(f"account {username} deleted note {title}")
                elif success == "Not Found": #note doest not exist
                    await websocket.send("None")
                    print(f"{username} tried deleting a note that doesn't exist")
                elif success == "incorrect": #incrorect details
                    await websocket.send("failed")
                    print(f"{username} tried deleting note: {title} with incorrect password")
                else: #unknown error
                    await websocket.send("err")
            
            elif message == "editNote": #editing a note
                message = json.loads(await websocket.recv())
                username = message["username"] 
                password = message["password"]
                title = message["title"]
                newContent = message["newContent"]
                newTitle = message["newTitle"]
                conORtitle = message["conORtitle"]

                success = app.editNote(username, password, title, newContent, newTitle, conORtitle)
                if success == "success": #edit success
                    await websocket.send("success")
                    print(f"account {username} edited note {title}")
                elif success == "exists": #note doest not exist
                    await websocket.send("exists")
                    print(f"{username} tried editing a note that doesn't exist")
                elif success == "incorrect": #incrorect details
                    await websocket.send("failed")
                    print(f"{username} tried editing note: {title} with incorrect password")
                elif success == "unknown call": #incrorect call for editing
                    await websocket.send("incorect call")
                    print(f"{username} tried editing note: {title} with incorrect call")
                else: #unknown error
                    await websocket.send("err")
            
            elif message == "getNotes": #getting notes
                message = json.loads(await websocket.recv())
                username = message["username"] 
                password = message["password"]

                success, notes = app.getNotes(username, password)
                if success == "success": #get success
                    await websocket.send("success")
                    print(f"account {username} got notes")
                    await websocket.send(json.dumps(notes))
                elif success == "failed": #incorrect details
                    await websocket.send("failed")
                    print(f"{username} tried getting notes with incorrect password")
                else: #unknown error
                    await websocket.send("err")

            else: #api call not recognized
                print(f"unknown api call: {message} disconnecting client")
                await websocket.send("err") #tell client to disconnect
                return

    except Exception as e: #error handling
        if str(e) != "no close frame received or sent":
            now = datetime.now()
            name = now.strftime("%H_%M_%S")
            print(f"ERROR OCCURED! saved error to logs, {name}")
            with open("logs/"+name+".txt","w") as f: #save log to file
                tb = traceback.format_exc()
                f.write(str(e)+"\n-----traceback-----\n"+str(tb))
        return

async def main():
    print("starting note server")
    async with serve(handler, "127.0.0.1", 8000):
        await asyncio.Future()  # run forever

asyncio.run(main())