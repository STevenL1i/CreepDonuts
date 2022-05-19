from datetime import datetime, timedelta

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class fb_db:

    def __init__(this, orgid:str):
        fyp_firebase = {
        "type": "service_account",
        "project_id": "fyp-22-s1-11",
        "private_key_id": "129c77c2f312dc4cea39c271a06bcd6b30e1354a",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCn+OrB41weLdey\nAcYOHAnXvWesR2FUgMfwVseM4/sW2rUHUWWAAMykVVjyts5aBmmgFc6dpqsR9s81\n3kdQi5CZvUfY3FNqmC8G3m5ugFJjmCY3UDxzZGtkEUuKelq8wB8CgV31yosdgLCU\nIoqod6PQpg6q8JBOxf7cYzbEzG5NiK1fyFlEEsEsqb7hv3TcOcAQ0TP+QIcRpIzS\nVrfpPFBWsgyhUL6dIacCuPgoo8SbgYHQs772QPiIiLTBfsn6C8diijfoffydjfQU\nUNRMs1uR/60uD79ScGBXIvhF7ct89+hzMazSN2DidiaZZepWuPB95N84Zux7rkoA\nYfI8C2hpAgMBAAECggEACfkCXx6TkosgOkZWrvHFN9Tb+eOHCNBYjpFoaZoDh1jW\n1KdlglMJ01vp2wc1eyzUSpfg24VQtNFVfhpDW6ndnPMa9+ok3bhJWnwMTG079wPK\niRAvdp5ordlFBeS7zGcPsENkA7rRxZ+lXDYsy1HHHRUu28FKoBKrTgRp9Qc6KUoy\nYRIQlEOZQMUHEi2VMGM5+qdJbhxZImBgoBLZPR/VBd99EwVN7rDlQmXdEC89I2m1\nVpobVf8uuTCWoUIyIBEpFpMS4qNmIlf+tc+kKLWFVp7rtO4o8ikR0mitWRTS8rJs\nSSq/nsIYNECC1DTl5dnPbXFbFon9Jl0QkWYDxdEPAQKBgQDiYFnXflI2Yzb6mGeD\naiMqVNhya5Rfrm6nVA6K95KsmkRIhW9q1Dd9Zqo8U/HN8Kmh49QF8zusC3ciejv+\nQqKrCQzfcjRWRSQgRw1+3/8dwckOClzhLHyu5RbxRWEqoZ1b82PqXpUgvs9/TyAQ\nYwe2mUJZ84HLqqSN1tluMQtToQKBgQC99AUyE2BAz773IX7vJRVPios0nlUYApfL\nze0IKuXUkuE8aRiYq5UYe/FLQY/+QaaL4yxPRp8kETawwCJE0uSo1bIln4VnmI2M\noG9Z4CA0VHChH38pqElbSonW24/7WoHDMzf2l5NRa4P5rm1zqRo2ljlZQrgDx1o0\nRP8QMV5fyQKBgEJh4raQcmdEfNDLdD9TFnDJZJdY+K9+JTCoM4OIydgXfMKPbnaz\nOHpraqw6KYQseHHirz/3bZ4r1omjsogC3lStWLsFcFeD+u4EJ+72nIcLVnvpigb1\n1rIqt6mUoMOxlMVr//awOabajVpVx59GivJ+yrg58evZZFu7jxMDCsFBAoGBAKu3\nZd7/7xqH8z1bNXGg12QBfZhCrfA3n9vou6ePiBcj9KN06nxRWEY6/UWn7jDOTm3V\nHuBHmmOzf/pGpnQLJhSOoi4qyCF/oi6HdkIMP3CvCOZPH9ibvjzd5D+sWrvB9N5u\ndd/g5JdNF5BmI6HUM9M2+H79tnYMCDqKSP3tc0ApAoGAKvLYyQmxBsg33xQND1Ls\nOjpjbVmUD8fT+iKyQ0i+69eJAfyZFUeI3uIrc5YZ3J2qa2zu8SkcbsBJep6+p6S5\nKJSPsVg1xpsQ7jtCUrMSemioPtfVn8UIZ6OLvCMZYYuZlHlys60bDh4Vf6lBV2aw\n18aIn/n040mo9k35iMQr9Vo=\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-ww43h@fyp-22-s1-11.iam.gserviceaccount.com",
        "client_id": "113796178287603754702",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-ww43h%40fyp-22-s1-11.iam.gserviceaccount.com"
        }
        this.orgid = orgid
        # use a service account
        cred = credentials.Certificate(fyp_firebase)
        firebase_admin.initialize_app(cred)
    
    def setupDetection(this, baseline:dict, rules:dict):
        db = firestore.client()
        doc_baseline = db.collection(f'{this.orgid}_detection').document("baseline")
        doc_baseline.set(baseline)
        doc_rules = db.collection(f'{this.orgid}_detection').document("rules")
        doc_rules.set(rules)

    def getlogBytime(this, time_from:datetime, time_to:datetime):
        db = firestore.client()
        query = db.collection(f'{this.orgid}_log').where("date", ">=", time_from).where("date", "<=", time_to).order_by("date", "ASCENDING")
        result = query.get()
        for i in range(0, len(result)):
            result[i] = result[i]._data
            result[i]["date"] = result[i]["date"].strftime("%Y-%m-%d %H:%M")
        return result

    def updatelog(this, minlog:dict, timestamp:str):
        db = firestore.client()
        log = db.collection(f'{this.orgid}_log').document(timestamp)
        log.set(minlog)

    def getOrgID(this, adminemail:str):
        db = firestore.client()
        query = db.collection("Admins Profile").where("Email", "==", adminemail)
        result = query.get()
        if len(result) == 0:
            return None
        else: 
            return result[0]._data["Organisation ID"], adminemail

    def getUserRules(this):
        db = firestore.client()
        doc = db.collection(f'{this.orgid}_detection').document("rules")
        result = doc.get().to_dict()
        return result
    
    def getBaseline(this):
        db = firestore.client()
        doc = db.collection(f'{this.orgid}_detection').document("baseline")
        result = doc.get().to_dict()
        return result

    def updateDetectionLog(this, anomaly:list, date:datetime, range:datetime, type:str):
        db = firestore.client()
        detectionLog = {"anomaly": anomaly,
                        "date": date,
                        "detection_range": range,
                        "detection_type": type,
                        "event_status": "standby"
                        }
        timestamp = date.strftime("%Y%m%d%H%M")
        doc = db.collection(f'{this.orgid}_detection').document(timestamp)
        doc.set(detectionLog)
        
    def getDetectionLog(this, detection_type:str, event_status:str):
        db = firestore.client()
        query = db.collection(f'{this.orgid}_detection').where("detection_type", "==", detection_type).where("event_status", "!=", event_status)
        result = query.get()
        return result