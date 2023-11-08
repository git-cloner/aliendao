## aliendao.cn文档

aliendao.cn（异形开源）是 huggingface.co（抱脸虫）资源的镜像网站，提供了常用的一些模型和数据集的下载服务。aliendao.cn的企业版e.aliendao.cn，提供了模型/数据集的下载、高性能聊天和推理API服务。

### 大语言模型相关文章

|         类别         | 链接                                                 | 说明                         |
| :-------------------: | ---------------------------------------------------- | ---------------------------- |
|        autogen        | https://zhuanlan.zhihu.com/p/663031095               | AutoGen+Chatglm2-6b实践（一）              |
| autogen | https://zhuanlan.zhihu.com/p/663238122 | AutoGen+Chatglm2-6b实践（二） |
| autogen | https://zhuanlan.zhihu.com/p/664598518 | AutoGen+Chatglm2-6b实践（三） |
| autogen | https://zhuanlan.zhihu.com/p/665328453 | AutoGen+Chatglm2-6b实践（四） |
| huggingface | https://huggingface.co/ | 全球最大的开源代码交流平台 |
| gitclone        		| https://gitclone.com                                 | 国内最大的github镜像网站     |
| aiit-chat       		| https://gitclone.com/aiit/chat/                      | gitclone发布的chat网站       |
| LLaMA2 | https://zhuanlan.zhihu.com/p/646811859 | LLaMA2中文微调 |
| LLaMA2 | https://zhuanlan.zhihu.com/p/645152512 | 在16G的推理卡上微调Llama-2-7b-chat |
| lama-lora-fine-tuning | https://github.com/git-cloner/llama-lora-fine-tuning | 低资源微调LLaMA，复现alpaca  |
|      alpaca-lora      | https://github.com/little51/alpaca-lora              | 低资源微调LLaMA，复现alpaca |
| FastChat | https://github.com/little51/FastChat | 部署Vicuna-7B |
| ChatGLM-6B | https://github.com/little51/ChatGLM-6B | 部署ChatGLM-6B |
| alpaca | https://zhuanlan.zhihu.com/p/638979593 | 使用deepspeed和lora复现alpaca |
| vicuna-7b | https://zhuanlan.zhihu.com/p/633469921 | 在单块16G的推理卡上微调复现vicuna-7b |
| FastChat | https://zhuanlan.zhihu.com/p/624286959 | FastChat+vicuna1.1部署与流式调用实践 |
| ChatGLM-6B | https://zhuanlan.zhihu.com/p/620233511 | 清华ChatGLM-6B模型实践 |
| ColossalAI | https://zhuanlan.zhihu.com/p/620070973 | ColossalAI推理实践 |
| Chinese-LLaMA-Alpaca | https://zhuanlan.zhihu.com/p/619954588 | Chinese-LLaMA-Alpaca实践 |
| 环境安装 | https://zhuanlan.zhihu.com/p/597063490 | linux安装nvidia驱动、cuda、conda（centos） |
| gpt-j-6b | https://zhuanlan.zhihu.com/p/594946225 | 在亚马逊aws的云主机上搭建gpt-j-6b模型 |
| gitclone | https://zhuanlan.zhihu.com/p/141597698 | 利用缓存加速从github clone |

### 下载过程FAQ

如果下载模型的速度很慢或无法下载，请按以下步骤查找问题：

- 判断本机到下载服务器是否通，使用以下命令确认

  telnet 61.133.217.139 20800

- 确认是否支付，因为异型岛企业版为付费下载服务，订单是与模型相关联的，一个订单只能下载一种模型

- 确保model_download.py为最新的，因为新的程序支持断点续传，如果发生意外断开可在上次下载的基础上继续下载

- 确认是否安装了conda环境，是否安装了huggingface_hub

- 如果wget、用脚本下载、从浏览器下载，都返回403，测说明token不对或未付费

### 大语言模型应用API

| 参数  | 说明                                                         |
| ----- | ------------------------------------------------------------ |
| URL   | https://chat.aliendao.cn/api/stream/v2?token=您的token       |
| token | 登录e.aliendao.cn后的个人中心可查看（https://e.aliendao.cn/#/user/center） |
| 请求  | POST，application/json                                       |

#### 发起

```json
{
    "context":{
        "prompt":"问题",
        "history":[
        ]
    },
    "modelname":"模型名称"
}
```

#### 说明

```shell
prompt：问题
history：二维数组，每一维是由问、答组成
modelname：有两个取值：ChatGLM-6b和Qwen-7b
```

#### 举例

```json
{
    "context":{
        "prompt":"你好",
        "history":[
            [
                "你好",
                "你好! 我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。"
            ],
            [
                "你好",
                "你好!有什么我可以都助你的吗"
            ]
        ]
    },
    "modelname":"ChatGLM-6b"
}
```

#### 返回

```json
{
    "response": "你好👋！我是人工智能助手 ChatGLM2-6B，很高兴见到你，欢迎问我任何问题。",
    "history": [
        [
            "你好",
            "你好👋！我是人工智能助手 ChatGLM2-6B，很高兴见到你，欢迎问我任何问题。"
        ]
    ],
    "status": 200,
    "time": 0.012832192936912179,
    "stop": true
}
```

**注意：需要多次调用，直到stop为true停止调用**