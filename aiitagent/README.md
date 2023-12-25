# Aiit-agent

## 1、Install env

```bash
conda create -n aliendao python=3.10 -y
conda activate aliendao
```

## 2、Run Local-LLMs

### 2.1、Install fastchat

```bash
git clone https://github.com/lm-sys/FastChat.git
cd FastChat
pip3 install --upgrade pip -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
pip3 install -e ".[model_worker,webui]" -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
pip3 install -y transformers
pip3 install transformers==4.30.2 -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
pip3 install torch==2.0.0+cu117 torchvision==0.15.1+cu117 torchaudio==2.0.1 --index-url https://download.pytorch.org/whl/cu117
pip3 install cpm_kernels -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
```

### 2.2、Run fastchat

```bash
python -m fastchat.serve.controller
CUDA_VISIBLE_DEVICES=1 python -m fastchat.serve.model_worker --model-path ../ChatGLM-6B
python -m fastchat.serve.openai_api_server --host 0.0.0.0 --port 8001
```

## 3、Intall pyautogen

```bash
git clone https://github.com/microsoft/autogen autogenv2
cp ./client.py autogenv2/autogen/oai/
cd autogenv2
# pip install openai==1.1.1 -i https://mirrors.aliyun.com/pypi/simple/
pip install fastapi -i https://mirrors.aliyun.com/pypi/simple/
pip install uvicorn -i https://mirrors.aliyun.com/pypi/simple/
pip install -e . -i https://mirrors.aliyun.com/pypi/simple/
pip install docker -i https://mirrors.aliyun.com/pypi/simple/
```

## 4、Run agent api server

```bash
python agent_api.py
```

