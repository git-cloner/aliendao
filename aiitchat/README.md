install

```shell
conda create -n aliendao python=3.10 -y
conda activate aliendao
pip install aiohttp==3.8.3 -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
pip install aiohttp_cors==0.7.0 -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
```

run backend

```shell
nohup python -u  aiitchat.py > aiitchat.log 2>&1 &
tail -f aiitchat.log
```

test webui

```shell
cd chat
npm start
```

build  webui

```shell
cd chat
npm run build
```

