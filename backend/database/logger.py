from datetime import datetime

def log(info_msg):
    date = datetime.now()
    date_string = date.strftime('[ %d-%m-%Y :: %H:%M:%S ] ')
    with open('DBQuery.log','a') as fd:
        fd.write(date_string+info_msg+'\n')

if __name__ == "__main__":
    pass