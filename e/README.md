## 异型岛企业版

e.aliendao.cn是异型岛（aliendao.cn）的企业版，相对于社区版，提供更多、更稳定、更快速的服务。
作者的新书：[大模型项目实战：多领域智能应用](https://github.com/little51/llm-dev)

### 一、服务介绍

- 大模型镜像快速下载：提供专用的带宽资源，实现更快、更稳定的huggingface模型下载。由于宽带资源有限，下载资源需要登录并支付流量包费用，价格约为 1元/G 。


 [Gemma](https://e.aliendao.cn/models/alpindale) [ChatGLM GLM4](https://e.aliendao.cn/models/THUDM)  [Qwen](https://e.aliendao.cn/models/Qwen)  [Stable-diffusion](https://e.aliendao.cn/models/stabilityai)  [Meta-llama](https://e.aliendao.cn/models/NousResearch)  [Baichuan](https://e.aliendao.cn/models/baichuan-inc)  [Thebloke](https://e.aliendao.cn/models/TheBloke)  [Microsoft](https://e.aliendao.cn/models/microsoft)  [Runwayml](https://e.aliendao.cn/models/runwayml)  [Openai](https://e.aliendao.cn/models/openai)  [FastChat](https://e.aliendao.cn/models/lmsys)  [EleutherAI](https://e.aliendao.cn/models/EleutherAI)  [Yi](https://e.aliendao.cn/models/01-ai)  [Google](https://e.aliendao.cn/models/google)  [Amazon](https://e.aliendao.cn/models/amazon)  [Bloom](https://e.aliendao.cn/models/bigscience)  [Llama-3](https://e.aliendao.cn/models/NousResearch)

- 客户服务请发邮件至 gitclone@126.com

### 二、使用说明

##### 方法1：用下载器  [model_download](https://e.aliendao.cn/model_download.py) 下载

```shell
pip install huggingface_hub
python model_download.py -e --repo_id 模型ID --token 用户token
# 例如
python model_download.py -e --repo_id Qwen/Qwen-7B --token KYmXxK0C0UfvFB1
# token在您登录e.aliendao.cn后的个人中心可查看（https://e.aliendao.cn/#/user/center）
# -e表示是企业版下载，下载地址有别于社区版
# model_download.py的获取：从本站首页点击文件链接，另存即可（不要复制链接下载！）
```

##### 方法2：从本站页面下载

从本站的models、datasets查找模型或数据集下载，下载时用复制按钮将下载网址复制到新的标签页下载，下载的url中带有token信息。

### 三、大模型装载方法

（1）将模型下载到本地文件夹

（2）AutoModel.from_pretrained的pretrained_model_name_or_path参数指向到本地文件夹

```python
# 以THUDM/chatglm-6b模型为例
# model_path = "THUDM/chatglm-6b" #从huggingface.co装载模型的方法
model_path = "./model/"           #从本地文件夹装载模型的方法
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_path,trust_remote_code=True).half().cuda()
```

### 四、其他说明

（1）e.aliendao.cn的模型资源还在持续同步中，如果模型文件夹中包含~incomplete.txt文件，说明正在同步中，镜像暂不可用

（2）请勿使用迅雷等工具下载

### 五、作者的新书

[图书官方直营：https://item.jd.com/14810472.html](https://item.jd.com/14810472.html)

![图书](https://gitclone.com/download1/llm-dev/llm-dev.png) ![网店链接](https://gitclone.com/download1/llm-dev/qr-code.png)