# 使用 Ubuntu 基础镜像  
FROM ubuntu:jammy-20240808

# 设置环境变量以避免交互模式  
ENV DEBIAN_FRONTEND=noninteractive  

# 安装 Python 3.11 和必要的工具  
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*  

# 设置 Python 3.11 为默认 python  
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1  

# 设置工作目录  
WORKDIR /workspace
# 拷贝本地文件到容器中
COPY chat_bot.py requirements.txt ./   

# 安装依赖库  
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/  

# 显示容器将使用的端口  
EXPOSE 8501 

# 启动 Streamlit 应用  
CMD ["streamlit", "run", "chat_bot.py"]

