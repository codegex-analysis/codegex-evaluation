#%%
import glob
from pathlib import Path
import json
import re
#%%
search_root = Path(__file__).resolve().parent / "files"
paths = glob.glob(f'{search_root}/**/files.json', recursive=True)

#%%
patrepo = re.compile(r"/files/([^/]+/[^/]+)/pulls/\d+/files.json")

#%%

repos = set()
for p in paths:
    repo_name = patrepo.search(p).group(1)  
    
    if repo_name in repos:
        continue
    
    with open(p, 'r') as jf:
        jfile = json.load(jf)
        for file in jfile:
            name = file['filename']
            if name.endswith('.java'):
                if 'patch' in file and file['status'] != 'removed':
                    repos.add(repo_name)
                    break

# %%
with open('repos.json', 'w') as out:
    json.dump(list(repos), out)
# %%
