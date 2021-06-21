import json

log = { 
    "userid": 1,
    "action": "create",
    "data": "user",
    "description": "Successfully create user on 20-06-12 02:14:58",
    "status": "success",
    "log_timestamp": "20-06-12 02:14:58"
    }

print(json.dumps(log))
