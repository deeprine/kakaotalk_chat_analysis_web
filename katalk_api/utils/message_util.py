from sanic.response import json as json_res
import json
import numpy as np

def json_default(value):
    if isinstance(value, np.int64):
        return int(value)
    elif isinstance(value, np.float64):
        return float(value)
    raise TypeError("not JSON serializable")

def get_error(data='', message=''):
    STATUS_ERROR = {}
    STATUS_ERROR['status'] = 'ERROR'
    STATUS_ERROR['message'] = '실패'
    STATUS_ERROR['data'] = 'error'

    if data:
        STATUS_ERROR['data'] = data
    if message:
        if isinstance(message, Exception):
            message = str(message)
        STATUS_ERROR['message'] = message

    dict1 = json.dumps(STATUS_ERROR, default=json_default)
    return json_res(dict1)

def get_success(data='', message=''):
    STATUS_OK = {}
    STATUS_OK['status'] = 'OK'
    STATUS_OK['message'] = '성공'
    STATUS_OK['data'] = 'success'

    if data:
        STATUS_OK['data'] = data
    if message:
        STATUS_OK['message'] = message

    dict1 = json.dumps(STATUS_OK, default=json_default)
    return json_res(dict1)

API_KEY_ERROR = get_error('', 'Invalid Key')