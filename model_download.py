# usage     : python ./model_download.py --repo_id repo_id
# example   : python ./model_download.py --repo_id facebook/opt-350m
import argparse
import time
import requests
import json
import os
from huggingface_hub import snapshot_download
import platform


def _log(_repo_id, _type, _msg):
    date1 = time.strftime('%Y-%m-%d %H:%M:%S')
    print(date1 + " " + _repo_id + " " + _type + " :" + _msg)


def _download_model(_repo_id):
    _local_dir = 'models/' + _repo_id
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
        snapshot_download(repo_id=_repo_id, cache_dir=_cache_dir, local_dir=_local_dir, local_dir_use_symlinks=_local_dir_use_symlinks,
                          resume_download=True)
    except Exception as e:
        error_msg = str(e)
        if ("401 Client Error" in error_msg):
            return True, error_msg
        else:
            return False, error_msg
    return True, ""


def _check_Completed(_repo_id, _local_dir):
    url = 'https://huggingface.co/api/models/' + _repo_id
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.text)
    else:
        return False
    for sibling in data["siblings"]:
        if not os.path.exists(_local_dir + "/" + sibling["rfilename"]):
            return False
    return True


def download_model_retry(_repo_id):
    i = 0
    flag = False
    msg = ""
    while True:
        flag, msg = _download_model(_repo_id)
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo_id', default=None, type=str, required=True)
    args = parser.parse_args()
    download_model_retry(args.repo_id)
