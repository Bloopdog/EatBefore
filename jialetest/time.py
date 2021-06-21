import datetime

def get_curr_time():
    # expected format: '2020-06-12 02:14:58'
    x = datetime.datetime.now()
    return (x.strftime("%Y-%m-%d %H:%M:%S"))

print (get_curr_time())