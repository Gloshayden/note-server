# Note Server
This is a note server that i made that expands on my previous C# notes app. i made this so i can create notes anywhere i want and for it to sync if i create a client for each device i use

# setup
## client
### CLI
to run the client you will need to copy the python file (either the code or from wget)
```
wget https://raw.githubusercontent.com/Gloshayden/note-server/refs/heads/main/app/CLI.py
```
then create the venv (if not globally)
```
python -m venv venv
source venv/bin/activate
```
to activate a venv in windows you need to do .\venv\scripts\activate
then insatll the packages required
```
pip install websocket && pip install cryptography
python CLI.py
```
### GUI
to run the GUI version you will need to copy the code and the requirements.txt
```
wget https://raw.githubusercontent.com/Gloshayden/note-server/refs/heads/main/app/GUI.py
wget https://raw.githubusercontent.com/Gloshayden/note-server/refs/heads/main/app/requirements.txt
```
then create a venv or install globaly if you dont want a venv
```
python -m venv venv
source venv/bin/activate
```
then install the requirements and run the app
```
pip install -r requirements.txt
python GUI.py
```
### Web GUI (experimental)
**Note: this is an experimental version and some elements my be broke**
to run the web GUI version you will need to copy the code and the requirements.txt
```
wget https://raw.githubusercontent.com/Gloshayden/note-server/refs/heads/main/app/GUIweb.py
wget https://raw.githubusercontent.com/Gloshayden/note-server/refs/heads/main/app/requirements.txt
```
then create a venv or install globaly if you dont want a venv
```
python -m venv venv
source venv/bin/activate
```
then install the requirements and run the app. You will need to install a different remi version
due to some broken dependencys
```
pip install -r requirements.txt
pip install remi==2021.3.2
python GUIweb.py
```
## server
to run the note server you will need to do the following steps
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
