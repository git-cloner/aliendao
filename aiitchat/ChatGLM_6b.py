import requests
import json
import datetime
import hashlib


def checkToken(token):
    if token is None:
        token = ""
    url = "http://172.16.62.157:8001/-/user/check_vip?token=" + token + '&sid=c'
    r = requests.get(url)
    return (r.status_code == 200)


def getAnswerFromChatGLM6b_v2(contextx, token):
    data = json.dumps(contextx)
    if checkToken(token):
        url = "http://172.16.62.137:8001/stream"
    else:
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
    return 'http://172.16.62.136:8000/stream'
    #hash = hash_string(prompt)[0]
    #if hash in "abcdefghijklm01234":
    #    return 'http://172.16.62.136:8000/stream'
    #else:
    #    return 'http://172.16.62.137:8001/stream'


def hash_string(text):
    data = bytes(text, encoding='utf-8')
    h = hashlib.md5(data).hexdigest()
    return h.lower()
