#%%
import json
from pathlib import Path
import pandas as pd
import os


DIR_CUR = Path(__file__).resolve().parent


def mark_new():
    """
    Add one column to xlsm tables which mark whether a instance belongs to new pattern set
    """
    with open(DIR_CUR / 'new_pattern_abbr.json', 'r') as f:
        new_patterns = set(json.load(f))
    
    dir_tab = DIR_CUR / 'tables'
    tables = os.listdir(dir_tab)
    for tab in tables:
        if not tab.endswith(".xlsm"):
            continue
        df = pd.read_excel(dir_tab / tab)
        col_name = "pattern" if tab == "matched-result.xlsm" else "type"
        df.insert(2, "isNew", df[col_name].isin(new_patterns))
        df.to_excel(dir_tab / tab.replace(".xlsm", ".xlsx"))

# %%
