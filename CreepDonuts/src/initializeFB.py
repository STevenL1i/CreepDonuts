import os
import sys
from datetime import datetime, timedelta

def main():
    orgid = sys.argv[1]
    import fb_db as fb
    fbins = fb.fb_db(orgid)

    baseline = {
        'lastupdate': datetime.now() - timedelta(hours=8),
        'range_ratio': {
            'usr_avg': 1,
            'sys_avg': 1,
            'idl_avg': 1,
            'idl_min': 4,
            'net_send': 1,
            'net_recv': 1,
            'disk_write': 1,
            'disk_read': 1
        },
        'weight': {
            'usr_avg': 1,
            'sys_avg': 1,
            'idl_avg': 2,
            'idl_min': 3,
            'disk_writ': 1,
            'disk_read': 1,
            'net_send': 4,
            'net_recv': 4
        },
        'threshold': {
            '5min': 1,
            '60min': 1,
            '30min': 1,
            '1440min': 1
        }
    }

    rules = {
        'net_recv': {'value': 0, 'enabled': False},
        'disk_read': {'value': 0, 'enabled': False},
        'net_send': {'value': 0, 'enabled': False},
        'disk_writ': {'value': 0, 'enabled': False},
        'CPU': {'maximum': 100, 'enabled': False}
    }

    fbins.setupDetection(baseline, rules)
    os.system("chmod +x initialize")
    os.system("./initialize")

if __name__ == "__main__":
    main()