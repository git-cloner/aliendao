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

## 3、制作Docker镜像

```bash
# 构建镜像
sudo docker build -t aicode .
# 测试镜像（交互式）
sudo docker run -p 8501:8501 -it aicode
# 测试镜像（后台服务）
sudo docker run -p 8501:8501 -d aicode
# 上传到本地镜像库（以本机IP=172.16.62.37为例）
# 本地镜像库：sudo docker run -d -p 5000:5000 --name registry registry:2
# 查看本地镜像库情况：http://172.16.62.37:5000/v2/_catalog
sudo docker tag aicode localhost:5000/aicode  
sudo docker push localhost:5000/aicode
# 在其他机器运行测试
sudo docker pull 172.16.62.37:5000/aicode
sudo docker run -p 8501:8501 -it 172.16.62.37:5000/aicode
```

