# download repositories according to top100_mvn_repo.txt to re-run the experiment

import subprocess
import os

from utils import path_root, path_top100_repos


url_sha_dict = dict()

def prepare_urls():
    path_top100_mvn_repo = path_root / "top100_mvn_repo.txt"
    with open(path_top100_mvn_repo, 'r') as f:
        lines = f.readlines()

    name_sha_dict = dict(line.strip().split(', ') for line in lines[104:204])

    for line in lines[:100]:
        url = line.strip()
        simple_name = url.split('/')[-1]
        if simple_name in name_sha_dict:
            url_sha_dict[url] = name_sha_dict[simple_name]
        else:
            print('Unmatch', url)


def download(url, parent_dir, sha=None):
    # if exist
    if url.split('/')[-1] in os.listdir(parent_dir):
        return

    p = subprocess.Popen(['git', 'clone', url], stdout=subprocess.PIPE, cwd=parent_dir)  # Asynchronous, non-blocking
    out, _ = p.communicate()  # block util p return
    out = out.decode()

    if 'fatal: ' in out: print('Download failed', url)


def checkout(path, sha):
    p = subprocess.Popen(['git', 'checkout', sha], stdout=subprocess.PIPE, cwd=path)
    out, _ = p.communicate()
    out = out.decode()
    if 'error: ' in out:
        print('Checkout failed', url)


if __name__ == '__main__':
    prepare_urls()

    for url, sha in url_sha_dict.items():
        download(url, path_top100_repos)
        path = path_top100_repos / url.split('/')[-1]
        checkout(path, sha)
