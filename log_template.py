# Expected json to be passed to log microservice:
# {   "microservice": "user",
#     "userid": 1,
#     "action": "create",
#     "data": "user",
#     "description": "Successfully create user on 20-06-12 02:14:58", 
#     "status": "success", 
#     "log_timestamp": "20-06-12 02:14:58"}

import json
import datetime
import amqp_setup
import pika

def get_curr_time():
    # expected format: '2020-06-12 02:14:58'
    x = datetime.datetime.now()
    x = x + datetime.timedelta(hours = 8)
    return (x.strftime("%Y-%m-%d %H:%M:%S"))

def create_log(microservice,userid,action,data,description,status):
    # allowed_actions = ['redeem','create','read','update','delete']
    # allowed_data = ['transaction','user','review','notification']
    curr_time = get_curr_time()

    log = { 
    'microservice': microservice,
    'userid': userid,
    'action': action,
    'data': data,
    'description': description,
    'status': status,
    'log_timestamp': curr_time
    }

    message = json.dumps(log)
    r_key = status + "." + microservice
    print('The routing key for this log is : \n' + r_key)
    amqp_setup.check_setup()

    amqp_setup.channel.basic_publish(
        exchange=amqp_setup.exchangename,
        routing_key=r_key, 
        body=message, 
        properties=pika.BasicProperties(delivery_mode = 2))
        # delivery_mode = 2 makes the message persistent

    return True