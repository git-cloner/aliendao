import requests
import json
import datetime
import hashlib

def getAnswerFromChatGLM6b_v2(contextx):
    data = json.dumps(contextx)
    url = get_bal_url(contextx["prompt"])
    headers = {'content-type': 'application/json;charset=utf-8'}
    r = requests.post(url, data=data, headers=headers)
    res = r.json()
    if r.status_code == 200:
        return res
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {'response': '算力不足，请稍候再试！[stop]', 'history': [], 'status': 200, 'time': now}


def get_bal_url(prompt):
    hash = hash_string(prompt)[0]
    if hash in "abcdefghijklm01234":
        return 'http://172.16.62.136:8000/stream'
    else:
        return 'http://172.16.62.137:8001/stream'


def hash_string(text):
    data = bytes(text, encoding='utf-8')
    h = hashlib.md5(data).hexdigest()
    return h.lower()
