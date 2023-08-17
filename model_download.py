# usage     : python model_download.py --repo_id repo_id --mirror
# example   : python model_download.py --repo_id facebook/opt-350m --mirror
import argparse
import time
import requests
import json
import os
from huggingface_hub import snapshot_download
import platform
from tqdm import tqdm
from urllib.request import urlretrieve


def _log(_repo_id, _type, _msg):
    date1 = time.strftime('%Y-%m-%d %H:%M:%S')
    print(date1 + " " + _repo_id + " " + _type + " :" + _msg)


def _download_model(_repo_id, _repo_type):
    if _repo_type == "model":
        _local_dir = 'dataroot/models/' + _repo_id
    else:
        _local_dir = 'dataroot/datasets/' + _repo_id
    try:
        if _check_Completed(_repo_id, _local_dir):
            return True, "check_Completed ok"
    except Exception as e:
        return False, "check_Complete exception," + str(e)
    _cache_dir = 'caches/' + _repo_id

    _local_dir_use_symlinks = True
    if platform.system().lower() == 'windows':
        _local_dir_use_symlinks = False
    try:
        if _repo_type == "model":
            snapshot_download(repo_id=_repo_id, cache_dir=_cache_dir, local_dir=_local_dir, local_dir_use_symlinks=_local_dir_use_symlinks,
                              resume_download=True, max_workers=2)
        else:
            snapshot_download(repo_id=_repo_id, cache_dir=_cache_dir, local_dir=_local_dir, local_dir_use_symlinks=_local_dir_use_symlinks,
                              resume_download=True, max_workers=2, repo_type="dataset")
    except Exception as e:
        error_msg = str(e)
        if ("401 Client Error" in error_msg):
            return True, error_msg
        else:
            return False, error_msg
    _removeHintFile(_local_dir)
    return True, ""


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


def _check_Completed(_repo_id, _local_dir):
    _writeHintFile(_local_dir)
    url = 'https://huggingface.co/api/models/' + _repo_id
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
    else:
        return False
    for sibling in data["siblings"]:
        if not os.path.exists(_local_dir + "/" + sibling["rfilename"]):
            return False
    _removeHintFile(_local_dir)
    return True


def download_model_retry(_repo_id, _repo_type):
    i = 0
    flag = False
    msg = ""
    while True:
        flag, msg = _download_model(_repo_id, _repo_type)
        if flag:
            _log(_repo_id, "success", msg)
            break
        else:
            _log(_repo_id, "fail", msg)
            if i > 1440:
                msg = "retry over one day"
                _log(_repo_id, "fail", msg)
                break
            timeout = 60
            time.sleep(timeout)
            i = i + 1
            _log(_repo_id, "retry", str(i))
    return flag, msg


def _fetchFileList(files):
    _files = []
    for file in files:
        if file['type'] == 'dir':
            filesUrl = 'https://www.aliendao.cn/' + file['path'] + '?json=true'
            response = requests.get(filesUrl)
            if response.status_code == 200:
                data = json.loads(response.text)
                for file1 in data['files']:
                    _files.append(file1)
        else:
            if file['name'] != '.gitattributes':
                _files.append(file)
    return _files


def _download_model_from_mirror(_repo_id, _repo_type):
    filesUrl = 'https://www.aliendao.cn/models/' + _repo_id + '?json=true'
    response = requests.get(filesUrl)
    if response.status_code != 200:
        _log(_repo_id, "mirror", str(response.status_code))
        return False
    data = json.loads(response.text)
    files = data['files']
    for file in files:
        if file['name'] == '~incomplete.txt':
            _log(_repo_id, "mirror", 'downloading')
            return False
    files = _fetchFileList(files)
    i = 1
    bar_format = '{desc}{percentage:3.0f}%|{bar}|{n_fmt}M/{total_fmt}M [{elapsed}<{remaining}, {rate_fmt}]'
    for file in files:
        url = 'http://61.133.217.142:20800/download/' + file['path']
        file_name = 'dataroot/' + file['path']
        response = requests.get(url, stream=True)
        data_size = round(
            int(response.headers['Content-Length']) / 1024 / 1024)
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
        _desc = str(i) + ' of ' + str(len(files)) + '(' + file['name'] + ')'
        i = i + 1
        with open(file_name, 'wb') as f:
            for data in tqdm(iterable=response.iter_content(1024 * 1024), total=data_size, desc=_desc, unit='MB', bar_format=bar_format):
                f.write(data)
    return True


def download_model_from_mirror(_repo_id, _repo_type):
    if _download_model_from_mirror(_repo_id, _repo_type):
        return
    else:
        return download_model_retry(_repo_id, _repo_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_id', default=None, type=str, required=True)
    parser.add_argument('--repo_type', default="model",
                        type=str, required=False)  # models,dataset
    parser.add_argument('--mirror', action='store_true')
    args = parser.parse_args()
    if args.mirror:
        download_model_from_mirror(args.repo_id, args.repo_type)
    else:
        download_model_retry(args.repo_id, args.repo_type)
