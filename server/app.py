import os,encryption,json,time

def register(username, password):
    if not os.path.exists("accounts/"+username):
        account = {"username":username,"password":password, "time": time.time}
        with open("accounts/"+username,"w") as f:
            json.dump(account,f)
        encryption.encryptFile("accounts/"+username)
        os.mkdir("notes/"+username)
        return "Created" 
    else: return "Exists"

def login(username, password):
    if os.path.exists("accounts/"+username):
        encryption.decryptFile("accounts/"+username)
        with open("accounts/"+username,"r") as f:
            account = json.load(f)
        encryption.encryptFile("accounts/"+username)
        if account["password"] == password:
            return account
        else: return "incorrect"
    else: return "unknown"

def createNote(username, password, title, content):
    note = {"title":title,"content":content}
    success = loadAccount(username, password)
    print(success)
    if success == "success":
        if os.path.exists(f"notes/{username}/{title}"):
            return "exists"
        else:
            with open(f"notes/{username}/{title}","w") as f:
                json.dump(note,f)
            encryption.encryptFile(f"notes/{username}/{title}")
            return "success"
    else: return "failed"

def readNote(username, password, title):
    success = loadAccount(username, password)
    print(success)
    if success == "success":
        if os.path.exists(f"notes/{username}/{title}"):
            encryption.decryptFile(f"notes/{username}/{title}")
            with open(f"notes/{username}/{title}","r") as f:
                content = f.read()
            encryption.encryptFile(f"notes/{username}/{title}")
            return content
        else: return "exists"
    else: return "failed"

def loadAccount(username, password):
    if os.path.exists("accounts/"+username):
        encryption.decryptFile("accounts/"+username)
        with open("accounts/"+username,"r") as f:
            account = json.load(f)
        encryption.encryptFile("accounts/"+username)
        if account["password"] == password:
            return "success", account
        else: return "incorrect"
    else: return "unknown"