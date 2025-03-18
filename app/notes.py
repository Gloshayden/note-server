import json, os

if os.path.exists("servers.json"):
    with open("servers.json","r") as f:
        servers = json.load(f)
else:
    servers = {}

print("Hi there welcome to the notes app!")
if servers == {}:
    print("You have no saved servers, please add one")
    print("the format has to be like this:")
    print("ws://serverip:port, example: ws://127.0.0.1:8000")
    print("server:")
    server = input()
    servers[server] = {}
    with open("servers.json","w") as f:
        json.dump(servers,f)