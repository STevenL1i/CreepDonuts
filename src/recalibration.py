from datetime import datetime, timedelta
import time
import traceback

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('fyp_firebase.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def updateStatus():
    pass


def recalibrate():
    pass


def main():
    now = datetime.today()
    now_str = now.strftime("%Y%m%d%H%M")
    lastmin = datetime.today() - timedelta(minutes=1)
    lastmin_str = lastmin.strftime("%Y%m%d%H%M")

    index = 0
    while True:
        if datetime.today().strftime("%Y%m%d%H%M") == now_str and index == 1:
            continue
        else:
            now = datetime.today()
            now_str = now.strftime("%Y%m%d%H%M")
            lastmin = datetime.today() - timedelta(minutes=1)
            lastmin_str = lastmin.strftime("%Y%m%d%H%M")


        ##### implementing analysis function below #####
        try:
            recalibrate()
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        ##### end implementation #####

        index = 1
        # detection interval (in second)
        time.sleep(300)

if __name__ == "__main__":
    main()