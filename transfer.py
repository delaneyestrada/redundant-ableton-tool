import os, sys, time
from notify_run import Notify
from transfer_set import transfer_set
from transfer_dir import transfer_dir

hostname = "LAPTOP-DANIEL"
username = "daniel_clanton@hotmail.com"
 # VARIABLES
    


try:
    func = sys.argv[1]
    password = sys.argv[2]
except:
    func = None
    while func not in ['all', 'set']:
        func = input("Transfer 'all' or 'set'? ")
    password = input("Enter Password: ")

timestr = time.strftime("%y%m%d-%H%M%S")

# GET ENDPOINT FROM TXT FILE
f = open("endpoint.txt", "r")
endpoint = f.read()
f.close()

notify = Notify(endpoint=endpoint)

# try:
source_paths = {
        'ableton': r'C:\Users\dillo\Desktop\Kyle Park Project',
        'dmxis': r'C:\Users\Public\Documents\ENTTEC\DMXIS\Shows\KP Show Testing'
    }
target_paths = {
        'ableton': r'C:/Users/danie/desktop/Kyle Park Project' + timestr,
        'dmxis': r'C:/Users/Public/Documents/ENTTEC/DMXIS/SHOWS/KP Show Testing'
    }

if func == "all":
    for key in target_paths.keys():
        transfer_dir(hostname, username, password, timestr, source_paths[key], target_paths[key])
if func == "set":
    source_paths['ableton'] = source_paths['ableton'] + r'\KP Show Copy.als'
    target_paths['ableton'] = r'C:/Users/danie/desktop/Kyle Park Project/KP Show Copy.als'

    transfer_set(hostname, username, password, timestr, source_paths['ableton'], target_paths['ableton'])
    transfer_dir(hostname, username, password, timestr, source_paths['dmxis'], target_paths['dmxis'])

pstools = r'C:\Users\dillo\Desktop\CODE\Tools\PSTools'
if(func == "set"):
    command = r'psexec \\' + hostname + r' -u ' +  username +  r' -p ' + password + r' -h -i -d cmd /c start "C:\ProgramData\Ableton\Live 10 Standard\Program\Ableton Live 10 Standard.exe" "C:\Users\danie\Desktop\Kyle Park Project\KP Show Copy.als"'
elif(func == "all"):
    command = r'psexec \\' + hostname + r' -u ' +  username +  r' -p ' + password + r' -h -i -d cmd /c start "C:\ProgramData\Ableton\Live 10 Standard\Program\Ableton Live 10 Standard.exe" "C:\Users\danie\Desktop\Kyle Park Project' + timestr + r'\KP Show Copy.als"'

# OPEN ABLETON
os.chdir(pstools)
os.system(command)

# SEND ANDROID NOTIFICATION
notify.send('File Transfer Script has run successfully')
print("Sent notification!")
# except:
#     notify.send("There was an issue with the File Transfer Script.")
#     print("Something went wrong!")