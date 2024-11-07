# Ollama for Linux快速安装

## 1、安装

```shell
# 使用以下命令，安装文件将从aliendao.cn下载
curl -fsSL https://aliendao.cn/ollama/install.sh | sh
# 配置公开访问
sudo vi /etc/systemd/system/ollama.service
在Service配置内增加：Environment="OLLAMA_HOST=0.0.0.0"
sudo systemctl daemon-reload 
sudo systemctl restart ollama   
# 查看日志
journalctl -u ollama -f
```

## 2、卸载

```shell
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /etc/systemd/system/ollama.service
sudo rm $(which ollama)
sudo rm -r /usr/share/ollama
sudo userdel ollama
sudo groupdel ollama
```

## 作者的新书

[图书官方直营：https://item.jd.com/14810472.html](https://item.jd.com/14810472.html)

![图书](https://gitclone.com/download1/llm-dev/llm-dev.png) ![网店链接](https://gitclone.com/download1/llm-dev/qr-code.png)