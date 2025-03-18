import os,encryption,json,time

def register(username, password):
    if not os.path.exists("accounts/"+username):
        account = {"username":username,"password":password,"created":time.time()}
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
            return "success"
        else: return "incorrect"
    else: return "unknown"

def createNote(username, password, title, content):
    note = {"title":title,"content":content}
    success, account = loadAccount(username, password)
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
    success, account = loadAccount(username, password)
    if success == "success":
        if os.path.exists(f"notes/{username}/{title}"):
            encryption.decryptFile(f"notes/{username}/{title}")
            with open(f"notes/{username}/{title}","r") as f:
                content = json.load(f)
            encryption.encryptFile(f"notes/{username}/{title}")
            return "success", content
        else: return "exists", "failed"
    else: return "failed", "failed"

def loadAccount(username, password):
    if os.path.exists("accounts/"+username):
        encryption.decryptFile("accounts/"+username)
        with open("accounts/"+username,"r") as f:
            account = json.load(f)
        encryption.encryptFile("accounts/"+username)
        if account["password"] == password:
            return "success", account
        else: return "incorrect", "failed"
    else: return "unknown", "failed"

def deleteNote(username, password, title):
    success, account = loadAccount(username, password)
    if success == "success":
        if os.path.exists(f"notes/{username}/{title}"):
            os.remove(f"notes/{username}/{title}")
            return "success"
        else: return "Not Found"
    else: return "incorrect"

def editNote(username, password, title, Newcontent, Newtitle, conORtitle):
    success, account = loadAccount(username, password)
    if success == "success":
        if conORtitle == "content":
            encryption.decryptFile(f"notes/{username}/{title}")
            note = {"title":title,"content":Newcontent}
            with open(f"notes/{username}/{title}","w") as f:
                json.dump(note,f)
            encryption.encryptFile(f"notes/{username}/{title}")
            return "success"
        elif conORtitle == "title":
            success, contents = readNote(username, password, title)
            content = contents["content"]
            encryption.decryptFile(f"notes/{username}/{title}")
            note = {"title":Newtitle,"content":content}
            os.rename(f"notes/{username}/{title}",f"notes/{username}/{Newtitle}")
            with open(f"notes/{username}/{Newtitle}","w") as f:
                json.dump(note,f)
            encryption.encryptFile(f"notes/{username}/{Newtitle}")
            return "success"
        else: return "unknown call"
    else: return "incorrect"