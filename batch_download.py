import time
import argparse

from model_download import download_model_retry
from model_mirror import make_mirror


def readTaskFromList(fn):
    x = -1
    z = 0
    model_id = ""
    with open(fn, 'r') as f:
        lines = f.readlines()
        z = len(lines)
        for i in range(len(lines)):
            line = lines[i]
            if line.startswith("*"):
                continue
            else:
                x = i
                model_id = line.strip()
                break
    return x, z, model_id


def writeFlagToList(fn, x):
    with open(fn, 'r') as f:
        lines = f.readlines()
    lines[x] = "*" + lines[x]
    with open(fn, 'w') as f:
        f.writelines(lines)


def downloadModelFromHg(model_id, repo_type):
    print("***** " + model_id + " *****")
    download_model_retry(model_id, repo_type)


def mirrorModel(_root, model_id, repo_type):
    print("***** " + model_id + " *****")
    make_mirror(_root, model_id, repo_type)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--listfile', default="model_list.txt", type=str, required=True)
    parser.add_argument(
        '--repo_type', default="model", type=str, required=False)
    parser.add_argument(
        '--mirror_root', default="", type=str, required=False)
    args = parser.parse_args()

    fn = args.listfile
    while True:
        x, z, model_id = readTaskFromList(fn)
        print(str(x+1) + ' of ' + str(z))
        if x == -1:
            time.sleep(10)
        else:
            if args.mirror_root != "":
                mirrorModel(args.mirror_root, model_id, args.repo_type)
            else:
                downloadModelFromHg(model_id, args.repo_type)
            writeFlagToList(fn, x)
            time.sleep(10)
