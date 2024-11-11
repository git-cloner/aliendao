# AI-Code-Test

## 1、环境

```shell
# 建立虚拟环境
conda create -n ai-code python=3.12 -y
# 激活虚拟环境
conda activate ai-code
# 安装依赖库
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

## 2、运行

```shell
# 激活虚拟环境
conda activate ai-code
# 运行Chat程序
streamlit run chat_bot.py
# 后台运行程序
nohup streamlit run chat_bot.py >aicode.log 2>&1 &
```

