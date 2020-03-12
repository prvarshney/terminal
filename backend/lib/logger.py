from datetime import datetime
import sys

def log(info_msg):
    date = datetime.now()
    date_string = date.strftime('[ %d-%m-%Y :: %H:%M:%S ] ')
    with open('DBQuery.log','a') as fd:
        fd.write(date_string+info_msg+'\n')
    sys.stderr.write(date_string+info_msg+'\n')
    sys.stderr.flush()
    # print((date_string+info_msg)
