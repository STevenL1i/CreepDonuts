import os
from os.path import exists
import sys
import csv
from datetime import datetime
from datetime import timedelta

"""
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('fyp_firebase.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
"""
def checkTaskStatus(taskname:str):
    taskcode = "0"
    # os.system("mkdir log")
    os.system(f'ps -ef | grep {taskname} > templog')
    task = open("log/temp", "r")
    stdin = task.read()
    if stdin.find("dstat -t") != -1:
        stdin = stdin[:stdin.find("dstat -t")]
        while True:
            if stdin.find("root") == -1:
                break
            
            stdin = stdin[stdin.find("root")+4:]
        
        while True:
            if stdin[0] == " ":
                stdin = stdin[1:]
            else:
                taskcode = stdin[:stdin.find(" ")]
                break
        
        os.system("rm -rf templog")
        return taskcode.replace(" ","")
        # os.system(f'kill -9 {taskcode}')

    else:
        os.system("rm -rf templog")
        return None

def killTask(taskcode:str):
    os.system(f'kill -9 {taskcode}')

def updatelog_local(minlog:dict, header:list):
    locallog = open("log/log_min", "a")
    writer = csv.DictWriter(locallog, fieldnames=header)
    writer.writerow({"datetime": (minlog["date"] + timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"),
                     "usr_min": minlog["usr"]["min"],
                     "usr_max": minlog["usr"]["max"],
                     "usr_avg": minlog["usr"]["avg"],
                     "sys_min": minlog["sys"]["min"],
                     "sys_max": minlog["sys"]["max"],
                     "sys_avg": minlog["sys"]["avg"],
                     "idling_min": minlog["idling"]["min"],
                     "idling_max": minlog["idling"]["max"],
                     "idling_avg": minlog["idling"]["avg"],
                     "disk_read": minlog["disk_read"].replace("M",""),
                     "disk_write": minlog["disk_write"].replace("M",""),
                     "net_recv": minlog["net_recv"].replace("M",""),
                     "net_send": minlog["net_send"].replace("M","")
                    })
    locallog.close()



orgid = sys.argv[1]

import fb_db as fb
fbins = fb.fb_db(orgid)



def collectlogs():
    """
    rawlog = open("log/log_raw", "w")
    rawlog.close()
    
    header = ["datetime", "usr_min", "usr_max", "usr_avg",
              "sys_min", "sys_max", "sys_avg",
              "idling_min", "idling_max", "idling_avg",
              "disk_read", "disk_write", "net_recv", "net_send"]
     
    if exists("log/log_min") == False:
        locallog = open("log/log_min", "w")
        writer = csv.DictWriter(locallog, fieldnames=header)
        writer.writeheader()
        locallog.close()
    """
    usr, sy, idl, wai, stl, read, writ, recv, send, pin, pout, sint, scsw = \
    [], [], [], [], [], [], [], [], [], [], [], [], []

    line = 0
    now_min = datetime.today().strftime("%Y-%m-%d %H:%M")
    while True:
        log = sys.stdin.readline()
        # rawlog = open("log/log_raw", "a")
        line += 1

        if line <= 3:
            # rawlog.write(log)
            # rawlog.close()
            continue
        
        """
        rawlog.write(log.replace("\n"," | "))
        rawlog.write(datetime.today().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        rawlog.close()
        """"""
        rawlog.write(log)
        rawlog.close()
        """
        
        
        # 0123456789012345678901234567890123456789012345678901234567890123456789
        # usr sys idl wai stl| read  writ| recv  send|  in   out | int   csw 
        #   1   1  98   0   0|  25k   36k|1375B 1312B|   0     0 |  12k   26k

        if now_min == datetime.today().strftime("%Y-%m-%d %H:%M"):
        # if (line-3) % 5 != 0:
            usr.append(int(log[0:3].replace(" ","")))
            sy.append(int(log[4:7].replace(" ","")))
            idl.append(int(log[8:11].replace(" ","")))
            wai.append(int(log[12:15].replace(" ","")))
            stl.append(int(log[16:19].replace(" ","")))
            # disk reads
            reads = int(log[20:24].replace(" ",""))
            if log[24] == "k" or log[25] == "K":
                reads = reads/1024
            elif log[24] == "B":
                reads = reads/1024/1024
            elif log[24] == "M":
                pass
            elif log[24] == "G":
                reads = reads*1024
            read.append(reads)
            # disk writes
            writes = int(log[26:30].replace(" ",""))
            if log[30] == "k" or log[30] == "K":
                writes = writes/1024
            elif log[30] == "B":
                writes = writes/1024/1024
            elif log[30] == "M":
                pass
            elif log[30] == "G":
                writes = writes*1024
            writ.append(writes)
            # network receives
            recevs = int(log[32:36].replace(" ",""))
            if log[36] == "k" or log[36] == "K":
                recevs = recevs/1024
            elif log[36] == "B":
                recevs = recevs/1024/1024
            elif log[36] == "M":
                pass
            elif log[36] == "G":
                recevs = recevs*1024
            recv.append(recevs)
            # network sends
            sends = int(log[38:42].replace(" ",""))
            if log[42] == "k" or log[42] == "K":
                sends = sends/1024
            elif log[42] == "B":
                sends = sends/1024/1024
            elif log[42] == "M":
                pass
            elif log[42] == "G":
                sends = sends*1024
            send.append(sends)

        else:
            now_min_log = datetime.today().strftime("%Y%m%d%H%M")
            for i in range(0,3):
                usr.remove(min(usr))
                usr.remove(max(usr))
                sy.remove(min(sy))
                sy.remove(max(sy))
                idl.remove(min(idl))
                idl.remove(max(idl))

            minlog = {
                "date": datetime.today() - timedelta(hours=8),
                "usr": {"min": min(usr),
                        "max": max(usr),
                        "avg": float(f'{sum(usr)/len(usr):.1f}')},
                "sys": {"min": min(sy),
                        "max": max(sy),
                        "avg": float(f'{sum(sy)/len(sy):.1f}')},
                "idling": {"min": min(idl),
                        "max": max(idl),
                        "avg": float(f'{sum(idl)/len(idl):.1f}')},
                "disk_read": f'{sum(read):.2f}M',
                "disk_write": f'{sum(writ):.2f}M',
                "net_recv": f'{sum(recv):.2f}M',
                "net_send": f'{sum(send):.2f}M'
            }
            
            fbins.updatelog(minlog, now_min_log)
            # updatelog_local(minlog, header)
            
            # for org in orgid:
            #     fb_db.fb_db.updatelog(minlog, now_min_log, org)

            now_min = datetime.today().strftime("%Y-%m-%d %H:%M")

            usr.clear()
            sy.clear()
            idl.clear()
            read.clear()
            writ.clear()
            recv.clear()
            send.clear()


def main():
    collectlogs()

if __name__ == "__main__":
    main()