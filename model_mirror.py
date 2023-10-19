# pip install beautifulsoup4 -i https://pypi.mirrors.ustc.edu.cn/simple --trusted-host=pypi.mirrors.ustc.edu.cn
# python model_mirror.py --root https://xxx.com --repo_id Open-Orca/LlongOrca-7B-16k

import requests
import argparse
from bs4 import BeautifulSoup
import subprocess
import os
import sys

all_links = set()


def get_links(url):
    if not url.endswith("/"):
        return
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        href = url + link.get('href')
        if href in all_links:
            return
        if not href.endswith("/"):
            # print(href)
            all_links.add(href)
        if href != url + "../":
            get_links(href)


def write_listfiles():
    with open('files.txt', 'w') as f:
        for link in all_links:
            f.write(link + '\n')


def _writeHintFile(_local_dir):
    file_path = _local_dir + '/~incomplete.txt'
    if not os.path.exists(file_path):
        if not os.path.exists(_local_dir):
            os.makedirs(_local_dir)
        open(file_path, 'w').close()


def _removeHintFile(_local_dir):
    file_path = _local_dir + '/~incomplete.txt'
    if os.path.exists(file_path):
        os.remove(file_path)


def download_files(_repo_id):
    _local_dir = 'dataroot/models/' + _repo_id
    _writeHintFile(_local_dir)
    command = ['aria2c', '-x', '16', '-c', '-d',
               _local_dir, '--input-file=files.txt']
    proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        print(line.decode(), end='')
        sys.stdout.flush()

    proc.wait()
    _removeHintFile(_local_dir)


def make_mirror(_root, repo_id):
    url = _root + "/download/models/" + repo_id + "/"
    get_links(url)
    write_listfiles()
    download_files(repo_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default=None, type=str, required=True)
    parser.add_argument('--repo_id', default=None, type=str, required=True)
    args = parser.parse_args()
    make_mirror(args.root, args.repo_id)
