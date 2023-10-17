import asyncio
import json
import time
import os
import aiohttp_cors
import requests
from aiohttp import web
from ChatGLM_6b import getAnswerFromChatGLM6b_v2
from Qwen_7b import getAnswerFromQwen7b_v2

filter_string = None


def filter_context(context):
    global filter_string
    if filter_string is None:
        print("loading filter")
        try:
            with open('filter.txt', mode='r', encoding='utf-8') as f:
                text = f.read().rstrip()
            filter_string = text.split('\n')
        except FileNotFoundError as err:
            filter_string = []
    for line in filter_string:
        if line in context:
            return True
    return False


def checkToken(token):
    if token is None:
        token = ""
    if token == "":
        token = ""
    url = "http://172.16.65.157:8001/-/user/check_vip?token=" + token + '&sid=c'
    r = requests.get(url)
    return (r.status_code == 200)


async def stream_v2(request):
    token = request.query.get('token')
    params = await request.json()
    context = params["context"]
    modelname = params["modelname"]
    prompt = context["prompt"]
    validtoken = checkToken(token)
    # filter
    if filter_context(prompt):
        return web.Response(
            content_type="application/json",
            text=json.dumps(
                {"response": "请更换问题重新输入",
                 "history": [],
                 "status": 403,
                 "time": 0,
                 "stop": True}
            ),
        )

    start = time.perf_counter()
    print(time.strftime("%Y-%m-%d %H:%M:%S",
          time.localtime()), "request : " + prompt)
    stop = False
    if modelname == 'Qwen-7b':
        result = getAnswerFromQwen7b_v2(context)
    else:
        result = getAnswerFromChatGLM6b_v2(context, validtoken)
    stop = result["response"] .endswith("[stop]")
    if result["response"] == "":
        result["response"] = "思考中"
    if stop:
        result["response"] = result["response"].replace("[stop]", "")
    if not validtoken:
        result["response"] = result["response"] + "[无效token]"
    end = time.perf_counter()
    result["time"] = end-start
    result["stop"] = stop
    print(time.strftime("%Y-%m-%d %H:%M:%S",
          time.localtime()), "result  : " + result["response"])
    return web.Response(
        content_type="application/json",
        text=json.dumps(result),
    )


app = web.Application()
cors = aiohttp_cors.setup(app)
app.router.add_post("/api/stream/v2", stream_v2)

for route in list(app.router.routes()):
    cors.add(route, {
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods="*"
        )
    })

if __name__ == "__main__":
    print("Start web server")
    web.run_app(
        app, access_log=None, host="0.0.0.0", port=5001, ssl_context=None
    )
