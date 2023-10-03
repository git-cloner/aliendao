### https://chat.aliendao.cn 源码

#### 1、后台

##### 1.1 install

```shell
conda create -n aliendao python=3.10 -y
conda activate aliendao
pip install aiohttp==3.8.3 -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
pip install aiohttp_cors==0.7.0 -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
```

##### 1.2 run

```shell
nohup python -u  aiitchat.py > aiitchat.log 2>&1 &
tail -f aiitchat.log
```

#### 2、前台

##### 2.1 test webui

```shell
cd chat
npm start
```

##### 2.2 build  webui

```shell
cd chat
npm run build
```

