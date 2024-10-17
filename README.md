# 从hf或Aliendao.cn镜像下载模型

## 1、简介

- 从hf下载模型（支持断点续传）
- 从aliendao.cn下载模型（支持断点续传）
- chat服务源码（调用国产大模型）
- 作者的新书
[图书官方直营：https://item.jd.com/14810472.html](https://item.jd.com/14810472.html)

![图书](https://gitclone.com/download1/llm-dev/llm-dev.png) ![网店链接](https://gitclone.com/download1/llm-dev/qr-code.png)

## 2、安装python虚拟环境

```bash
# windows到Anaconda官网下载安装
# Linux用以下方法安装
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
chmod +x Anaconda3-2022.10-Linux-x86_64.sh
./Anaconda3-2022.10-Linux-x86_64.sh
source ~/.bashrc
```

## 3、创建虚拟环境

```bash
git clone https://github.com/git-cloner/aliendao
cd aliendao
conda create -n aliendao python=3.10 -y
conda activate aliendao
pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
```

## 4、下载

```bash
conda activate aliendao
# 下载模型，带上mirror优先从镜像下载
python model_download.py --repo_id 模型ID
# 举例
python model_download.py --repo_id baichuan-inc/Baichuan-7B
# 下载数据集
python model_download.py --repo_id 数据集ID --repo_type dataset
# 举例
python model_download.py --repo_id tatsu-lab/alpaca --repo_type dataset

```

