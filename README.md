# Note Server
This is a note server that i made that expands on my previous C# notes app. i made this so i can create notes anywhere i want and for it to sync if i create a client for each device i use

# setup
## client
to run the client you will need to copy the python file (either the code or from wget)
```
wget https://raw.githubusercontent.com/Gloshayden/note-server/refs/heads/main/app/notes.py
```
then create the venv (if not globally)
```
venv -m venv venv
source venv/bin/activate
```
then insatll the packages required
```
pip install websocket && pip install cryptography
python notes.py
```
## server
to run the note server you wwill need to do the following steps
clone the git
```
git clone https://github.com/Gloshayden/note-server.git
cd note-server/server
```
then if you want, create a venv
```
python -m venv venv
source venv/bin/activate
```
install requirements
```
pip install -r requirements.txt
```
and run the server
```
python server.py
```
