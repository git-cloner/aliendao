## 异型岛企业版

e.aliendao.cn是异型岛（aliendao.cn）的企业版，相对于社区版，提供更多、更稳定、更快速的服务。

### 一、服务介绍

#### 1、大模型镜像快速下载

提供专用的带宽资源，实现更快、更稳定的huggingface模型下载。

#### 2、GPU推理服务

提供web版的chat服务[https://chat.aliendao.cn](https://chat.aliendao.cn) 及API，使用专用的GPU资源。

#### 3、客户服务

请发邮件至 gitclone@126.com

### 二、使用说明

#### 1、大模型镜像

##### 方法1：用下载器下载

```shell
pip install huggingface_hub
python model_download.py --repo_id 模型ID --mirror --token 用户token
# 例如
python model_download.py --repo_id Qwen/Qwen-7B --mirror --token KYmXxK0C0UfvFB1
# token在您登录e.aliendao.cn后的个人中心可查看（https://e.aliendao.cn/#/user/center）
```

##### 方法2：从本站页面下载

从本站的models、datasets查找模型或数据集下载，下载时用复制按钮将下载网址复制到新的标签页下载，下载的url中带有token信息。

#### 2、Aiit-Chat

[https://e.aliendao.cn/document](https://e.aliendao.cn/document)

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
