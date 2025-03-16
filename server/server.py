import asyncio, os, random, traceback, encryption
from websockets.server import serve
from datetime import datetime
from cryptography.fernet import Fernet


if os.path.exists("logs") == False: os.mkdir("logs")
if os.path.exists("accounts") == False: os.mkdir("accounts")
if os.path.exists("notes") == False: os.mkdir("notes")
if os.path.exists("key.key") == False:
    key = Fernet.generate_key()
    with open("key.key","xb") as f:
        f.write(key)

def login(username, password):
    return

with open("key.key","rb") as f:
    keyinfo = f.read()
key = Fernet(keyinfo)
tstenc = encryption.encryptString("test",keyinfo)
print(tstenc)
testdec = encryption.decryptString(tstenc,keyinfo)
print(testdec)
'''async def handler(websocket):
    try:
        async for message in websocket:
            if message == "close": #closing websocket
                await websocket.send("goodbye")
                return
            elif message == "login": #logging in
                await websocket.send("logged in")
                return

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

asyncio.run(main())'''