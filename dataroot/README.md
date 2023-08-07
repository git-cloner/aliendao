## 大语言模型下载站

HuggingFace.co资源下载网站，为开发者提供模型镜像加速服务。

### 1、模型下载方法

#### 方法1：用下载器下载

```bash
pip install huggingface_hub
python model_download.py --repo_id 模型ID --mirror
# 举例
python model_download.py --repo_id THUDM/chatglm2-6b --mirror
# 详细用法见：https://github.com/git-cloner/aliendao 
```

#### 方法2：从本站页面下载

从本站的models、datasets查找模型或数据集下载，下载时建议用复制按钮将下载网址复制到新的标签页下载，这样速度更快。

### 2、型装载方法

（1）将模型下载到本地文件夹

（2）AutoModel.from_pretrained的pretrained_model_name_or_path参数指向到本地文件夹

```python
# 以THUDM/chatglm-6b模型为例
# model_path = "THUDM/chatglm-6b" #从huggingface.co装载模型的方法
model_path = "./model/"           #从本地文件夹装载模型的方法
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModel.from_pretrained(model_path,trust_remote_code=True).half().cuda()
```

### 3、其他说明

（1）aliendao.cn的模型资源还在持续同步中，如果模型文件夹中包含~incomplete.txt文件，说明正在同步中，镜像不可用

（2）请勿使用迅雷等工具下载