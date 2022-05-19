import os

import fb_db as fb
fbins = fb.fb_db("")

def getOrgID():
    while True:
        # ask user to enter his admin account (email)
        adminemail = input("Please enter your email(type \"quit\" to exit): ")
        if adminemail == "quit":
            exit(0)
        # adminemail = "admin1@gmail.com"
        # find the organization id of the admin's email
        orgid = fbins.getOrgID(adminemail)
        if orgid == None:
            input("Your account is not found, please retry......")
        else: 
            return orgid

def initializeIDS(orgid:str):
    os.system(f'python3 src/initializeFB.py {orgid}')

def startlogging(orgid:str):
    os.system(f'nohup dstat | python3 src/log.py {orgid} &')

def startAnalysis(orgid:str):
    os.system(f'nohup python3 src/detection.py {orgid} &')

def checkstatus(orgid:str):
    os.system("ps -ef | grep python3 > temp")
    f = open("temp", "r")
    stdout = f.read()
    print(f'{"Service":<20}{"Status"}')
    if stdout.find(f'log.py {orgid}') != -1:
        print(f'{"Logging":<20}{"ACTIVE"}')
    else:
        print(f'{"Logging":<20}{"OFFLINE"}')

    if stdout.find(f'detection.py {orgid}') != -1:
        print(f'{"Analysis":<20}{"ACTIVE"}')
    else:
        print(f'{"Analysis":<20}{"OFFLINE"}')
    print()
    f.close()
    os.system("rm -rf temp")