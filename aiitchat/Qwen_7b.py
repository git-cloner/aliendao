import requests
import json
import datetime


def getAnswerFromQwen7b_v2(contextx):
    data = json.dumps(contextx)
    url = 'http://172.16.62.66:8008/stream'
    headers = {'content-type': 'application/json;charset=utf-8'}
    r = requests.post(url, data=data, headers=headers)
    res = r.json()
    if r.status_code == 200:
        return res
    else:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return {'response': '算力不足，请稍候再试！[stop]', 'history': [], 'status': 200, 'time': now}
