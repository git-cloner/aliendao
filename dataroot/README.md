## 异型岛社区版

异型岛社区版是HuggingFace资源下载网站，为AI开发者提供模型下载服务，通过下载器可以提高下载速度，解决大模型下载时间长、经常断线、需要反复重试等问题，实现镜像加速、断点续传、无人值守下载。本项目下载器、Chat服务的源码在 [github.com/git-cloner/aliendao](https://github.com/git-cloner/aliendao)

#### 请访问 [异型岛企业版](https://e.aliendao.cn) 获得更好的体验

- 更多、更全、更新的Model
- 更多、更全、更新的Dataset
- 更快下载速度（*2M/s ~ **40**M/s*）
- 节省您的宝贵时间
- [ChatGLM](https://e.aliendao.cn/models/THUDM)  [Qwen](https://e.aliendao.cn/models/Qwen)  [Stable-diffusion](https://e.aliendao.cn/models/stabilityai)  [Meta-llama](https://e.aliendao.cn/models/NousResearch)  [Baichuan](https://e.aliendao.cn/models/baichuan-inc)  [Thebloke](https://e.aliendao.cn/models/TheBloke)  [Microsoft](https://e.aliendao.cn/models/microsoft)  [Runwayml](https://e.aliendao.cn/models/runwayml)  [Openai](https://e.aliendao.cn/models/openai)  [FastChat](https://e.aliendao.cn/models/lmsys)  [EleutherAI](https://e.aliendao.cn/models/EleutherAI)  [Yi](https://e.aliendao.cn/models/01-ai)  [Google](https://e.aliendao.cn/models/google)  [Amazon](https://e.aliendao.cn/models/amazon)  [Bloom](https://e.aliendao.cn/models/bigscience)

### 1、模型下载方法

#### 方法1：用下载器  [model_donwload.py](https://e.aliendao.cn/model_download.py) 下载

```bash
pip install huggingface_hub
python model_download.py --repo_id 模型ID
# 例如
python model_download.py --repo_id Qwen/Qwen-7B
```

![](https://gitclone.com/download1/aliendao/aliendao.gif)

#### 方法2：从本站页面下载

从本站的models、datasets查找模型或数据集下载，下载时用复制按钮将下载网址复制到新的标签页下载。

### 2、模型装载方法

（1）将模型下载到本地文件夹

（2）AutoModel.from_pretrained的pretrained_model_name_or_path参数指向到本地文件夹

```python
# 以THUDM/chatglm-6b模型为例
# model_path = "THUDM/chatglm-6b" #从huggingface.co装载模型的方法
model_path = "./model/"           #从本地文件夹装载模型的方法
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_path,trust_remote_code=True).half().cuda()
```

### 3、重要提醒

（1）开源资源有限，网站对每个IP限制了两个并发连接

（2）请勿使用迅雷等工具下载，Trident、Transmission、netdisk等下载任务将被拦截

（3）下载如有问题，请联系gitclone@126.com