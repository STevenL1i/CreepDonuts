import sys
import time
from datetime import datetime, timedelta
import traceback

import json
import pandas
import numpy
from sklearn.metrics import r2_score

orgid = sys.argv[1]

import fb_db as fb
fbins = fb.fb_db(orgid)


def analysis(time_from:datetime, time_to:datetime, period:int):
    log = fbins.getlogBytime(time_from, time_to)
    x = []
    y = {
        "usr_avg": [],
        "sys_avg": [],
        "idl_avg": [],
        "idl_min": [],
        "net_send": [],
        "net_recv": [],
        "disk_read": [],
        "disk_write": []
    }
    
    for i in range(0, int(len(log)/period)):
        x.append(i)
        tempy = {
        "usr_avg": [],
        "sys_avg": [],
        "idl_avg": [],
        "idl_min": [],
        "net_send": [],
        "net_recv": [],
        "disk_read": [],
        "disk_write": []
        }
        for j in range(0,period):
            # templist.append(float(log[i*period+j]["net_send"].replace("M","")))
            # templist.append(float(log[i*period+j]["sys"]["avg"]))
            tempy["usr_avg"].append(float(log[i*period+j]["usr"]["avg"]))
            tempy["sys_avg"].append(float(log[i*period+j]["sys"]["avg"]))
            tempy["idl_avg"].append(float(log[i*period+j]["idling"]["avg"]))
            tempy["idl_min"].append(float(log[i*period+j]["idling"]["min"]))
            tempy["net_send"].append(float(log[i*period+j]["net_send"].replace("M","")))
            tempy["net_recv"].append(float(log[i*period+j]["net_recv"].replace("M","")))
            tempy["disk_read"].append(float(log[i*period+j]["disk_read"].replace("M","")))
            tempy["disk_write"].append(float(log[i*period+j]["disk_write"].replace("M","")))

        field = tempy.keys()
        for f in field:
            y[f].append(tempy[f])

    field = tempy.keys()
    for f in field:
        for i in range(0, len(y[f])):
            mean = numpy.mean(y[f][i])
            y[f][i] = mean



    analysisLog = {
        "time_from": time_from.strftime("%Y-%m-%d %H:%M"),
        "time_to": time_to.strftime("%Y-%m-%d %H:%M"),
        "period": period,
    }

    for i in range(0, 2):
        x.remove(max(x))
        for f in field:
            y[f].remove(max(y[f]))

    for f in field:
        mymodel = numpy.poly1d(numpy.polyfit(x, y[f], 3))

        relation_index = r2_score(y[f], mymodel(x))

        future = mymodel(x[-1]+1)

        analysisLog[f] = {"relation_index": relation_index, "predict": future}
    
    """
    with open("analysisLog.json", "w") as anly:
        json.dump(analysisLog, anly)
    """
    
    return analysisLog


def alertengine(analysisLog:dict):
    """
    # get the logs from counter.json
    with open("analysisLog.json") as analog:
        analysisLog = json.load(analog)
    """
    time1 = datetime.strptime(analysisLog["time_from"], "%Y-%m-%d %H:%M")
    time2 = datetime.strptime(analysisLog["time_to"], "%Y-%m-%d %H:%M")
    time3 = time2 + timedelta(minutes=analysisLog["period"])
    log_raw = fbins.getlogBytime(time2, time3)
    log = {
        "usr_avg": [],
        "sys_avg": [],
        "idl_avg": [],
        "idl_min": [],
        "net_send": [],
        "net_recv": [],
        "disk_read": [],
        "disk_write": []
    }
    for l in log_raw:
        log["usr_avg"].append(float(l["usr"]["avg"]))
        log["sys_avg"].append(float(l["sys"]["avg"]))
        log["idl_avg"].append(float(l["idling"]["avg"]))
        log["idl_min"].append(float(l["idling"]["min"]))
        log["net_send"].append(float(l["net_send"].replace("M","")))
        log["net_recv"].append(float(l["net_recv"].replace("M","")))
        log["disk_read"].append(float(l["disk_read"].replace("M","")))
        log["disk_write"].append(float(l["disk_write"].replace("M","")))
    
    # get user's rules
    rules = fbins.getUserRules()
    rules_field = rules.keys()
    for f in rules_field:
        if rules[f]["enabled"] == True:
            try:
                maxvalue = max(log[f])
                log[f] = maxvalue
            except KeyError:
                minvalue = min(log["idl_min"])
                log["idl_min"] = minvalue

    # get baseline
    baseline = fbins.getBaseline()
    
    all_field = log.keys()
    counter = []
    anomaly = []
    for f in all_field:
        if type(log[f]) == list:
            relation_index = analysisLog[f]["relation_index"]
            predict = analysisLog[f]["predict"]
            real = numpy.mean(log[f])
            floating = predict / relation_index
            range_ratio = baseline["range_ratio"][f]
            range0 = predict - floating - (floating * range_ratio)
            range1 = predict + floating + (floating * range_ratio)
            if real > range1:
                counter.append((real - range1) * baseline["weight"][f])
            elif real < range0:
                counter.append((range0 - real) * baseline["weight"][f])

        else:
            try:
                real = log[f]
                value = rules[f]["value"]
                if real > value:
                    anomaly.append(f)
            except KeyError:
                real = log[f]
                value = 100 - rules["CPU"]["maximum"]
                if real < value:
                    anomaly.append("CPU")
    
    try:
        counter_ratio = numpy.mean(counter)
        if counter_ratio > baseline["threshold"][f'{analysisLog["period"]}min']:
            anomaly.append("System analysis")
    except KeyError:
        if counter_ratio > baseline["threshold"][f'60min']:
            anomaly.append("System analysis")
    
    if len(anomaly) > 0:
        time_from = datetime.strptime(analysisLog["time_from"], "%Y-%m-%d %H:%M")
        time_to = datetime.strptime(analysisLog["time_to"], "%Y-%m-%d %H:%M")
        time_anomaly = time_to + timedelta(minutes=analysisLog["period"])
        if "System analysis" in anomaly:
            detetion_type = "System analysis"
        else:
            detection_type = "User settings"
        fbins.updateDetectionLog(anomaly, time_anomaly, time_from, detection_type)



def main():
    now = datetime.today()
    now_str = now.strftime("%Y%m%d%H%M")
    lastmin = datetime.today() - timedelta(minutes=5)
    lastmin_str = lastmin.strftime("%Y%m%d%H%M")

    index = 0
    while True:
        now = datetime.today()
        now_min = int(now.strftime("%M"))
        """ if datetime.today().strftime("%Y%m%d%H%M") == now_str and index == 1:
            continue """
        if now_min % 5 != 0 or index == 1:
            nowtemp = datetime.today()
            targettemp = nowtemp + timedelta(minutes=(5 - now_min % 5))
            target = datetime(targettemp.year, targettemp.month, targettemp.day, targettemp.hour, targettemp.minute, 0)
            sleeptime = (target - nowtemp).seconds + 1
            time.sleep(sleeptime)
        """
        else:
            now = datetime.today()
            lastmin = datetime.today() - timedelta(minutes=5)
        """


        ##### implementing analysis function below #####

        try:
            now = datetime.today() - timedelta(hours=8)
            if int(now.strftime("%M")) % 5 == 0:
                alertengine(analysis(now-timedelta(minutes=65), now-timedelta(minutes=5), 5))
            if int(now.strftime("%M")) % 30 == 0:
                alertengine(analysis(now-timedelta(hours=12.5), now-timedelta(minutes=30), 30))
            if int(now.strftime("%M")) == 0:
                alertengine(analysis(now-timedelta(hours=25), now-timedelta(hours=1), 60))
            if int(now.strftime("%H")) == 0:
                alertengine(analysis(now-timedelta(days=8), now-timedelta(days=1), 1440))
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        ##### end implementation #####

        index = 1
        # detection interval (in second)
        # time.sleep(300)

if __name__ == "__main__":
    main()