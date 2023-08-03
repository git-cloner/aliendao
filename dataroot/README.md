### 大语言模型下载站

HuggingFace.co资源下载网站，为开发者提供模型镜像加速服务。

#### 模型下载方法

**方法1：**从本站下载

- 操作：从本站的models、datasets查找模型或数据集下载

- 优点：无其他依赖，使用方便
- 缺点：速度略慢

**方法2：**用下载器下载

- 操作：按用 https://github.com/git-cloner/aliendao 方法从huggingface官网断点续传下载，简单来说，就是运行：python model_download.py --repo_id 模型ID

- 优点：下载速度快
- 缺点：依赖python和huggingface_hub

#### 模型装载方法

（1）将模型下载到本地文件夹

（2）AutoModel.from_pretrained的pretrained_model_name_or_path参数指向到本地文件夹

```python
# 以THUDM/chatglm-6b模型为例

# model_path = "THUDM/chatglm-6b" #从huggingface.co装载模型的方法
model_path = "./model/"           #从本地文件夹装载模型的方法
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_path,trust_remote_code=True).half().cuda()
```

#### 其他说明

（1）aliendao.cn的模型资源还在持续同步中，如果模型文件夹中包含~incomplete.txt文件，说明正在同步中，镜像不可用

（2）请勿使用迅雷等工具下载