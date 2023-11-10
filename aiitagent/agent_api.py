from fastapi import FastAPI, Request
import autogen
import uvicorn
import json
import datetime
import threading
import builtins
from autogen.oai.client import stream_buffer

app = FastAPI()


def stream_item(prompt, history):
    config_list_gpt = [
        {
            "model": "ChatGLM-6B",
            "base_url": "http://172.16.62.137:8001/v1",
            "api_key": "NULL",
        }
    ]
    llm_config = {"config_list": config_list_gpt,
                  "stream": True, "timeout": 600}

    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
        human_input_mode="NEVER"
    )
    coder = autogen.AssistantAgent(
        name="Coder",
        llm_config=llm_config
    )
    pm = autogen.AssistantAgent(
        name="Product_manager",
        system_message="Creative in software product ideas.",
        llm_config=llm_config,
    )

    groupchat = autogen.GroupChat(
        agents=[user_proxy, coder, pm], messages=[], max_round=5)
    manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config)
    user_proxy.initiate_chat(
        manager, message=prompt)
    stream_buffer[prompt]["stop"] = True


def removeTimeoutBuffer():
    for key in stream_buffer.copy():
        diff = datetime.datetime.now() - stream_buffer[key]["time"]
        seconds = diff.total_seconds()
        print(key + ": 已存在" + str(seconds) + "秒")
        if seconds > 1200:
            if stream_buffer[key]["stop"]:
                del stream_buffer[key]
                print(key + "：已被从缓存中移除")
            else:
                stream_buffer[key]["stop"] = True
                print(key + "：已被标识为结束")


@app.post("/stream")
async def create_item(request: Request):
    # 删除过期的buffer
    removeTimeoutBuffer()
    # 获取入参
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    # 判断是否已在生成，只有首次才调stream_chat
    now = datetime.datetime.now()
    if prompt == '你好':
        return {
            "response": "您好，我是Aiit智体，基于Autogen构建，可以使用多个角色会话回答您在编程方面的问题。[stop]",
            "history": [],
            "status": 200,
            "time": now.strftime("%Y-%m-%d %H:%M:%S")
        }
    if stream_buffer.get(prompt) is None:
        stream_buffer[prompt] = {"response": "",
                                 "stop": False, "history": [], "time": now}
        # 在线程中调用stream_chat
        sub_thread = threading.Thread(
            target=stream_item, args=(prompt, history))
        sub_thread.start()
    # 异步返回response
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    response = stream_buffer[prompt]["response"]
    history = stream_buffer[prompt]["history"]
    # 如果stream_chat调用完成，给返回加一个停止词[stop]
    if stream_buffer[prompt]["stop"]:
        response = response + '[stop]'
    answer = {
        "response": response,
        "history": history,
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", prompt:"' + \
        prompt + '", response:"' + repr(response) + '"'
    # print(log)

    return answer


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8006, workers=1)
