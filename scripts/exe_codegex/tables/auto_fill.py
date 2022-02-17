#%%
from operator import index
from pathlib import Path
import pandas as pd
import json

DIR_CUR = Path(__file__).resolve().parent

df_match = pd.read_csv(DIR_CUR / "csv" / "matched-result.csv")
df_rbugs_unmatch = pd.read_csv(DIR_CUR / "csv" / "rbugs-unmatched-result.csv", header=None, names=('project name','pattern','path','lineno','content'))
df_spotbugs_unmatch = pd.read_csv(DIR_CUR / "csv" / "spotbugs-unmatched-result.csv", header=None, names=('project name','pattern','path','lineno'))


def mark_new():
    """
    Add one column to indicate whether a instance belongs to new pattern set
    """
    with open(DIR_CUR / 'new_pattern_abbr.json', 'r') as f:
        new_patterns = set(json.load(f))

    for df in (df_match, df_rbugs_unmatch, df_spotbugs_unmatch):
        if 'isNew' not in df:
            df.insert(2, "isNew", df['pattern'].isin(new_patterns))

#%%
def auto_fill_new():
    path_workbook = DIR_CUR / "old" / "manual-label-new.xlsx"
    df_new_match = pd.read_excel(path_workbook, sheet_name="matched")
    df_new_rbugs_unmatch = pd.read_excel(path_workbook, sheet_name="codegex-unmatched")
    df_new_spotbugs_unmatch = pd.read_excel(path_workbook, sheet_name="spotbugs-unmatched")

    df_new_rbugs_unmatch = df_new_rbugs_unmatch.loc[df_new_rbugs_unmatch.isNew]
    df_new_spotbugs_unmatch = df_new_spotbugs_unmatch.loc[df_new_spotbugs_unmatch.isNew]

    for _, row in df_new_rbugs_unmatch.iterrows():
        df_rbugs_unmatch.loc[(df_rbugs_unmatch.pattern == row['type']) & (df_rbugs_unmatch.path == row['path']) & (df_rbugs_unmatch.lineno == row['line no']), ["Is our FP?", "Is SP's FN?", 'label limitation (spotbugs)', 'Note']] = [row["Is our FP?"], row["Is SP's FN?"], row['label limitation (spotbugs)'], row['Note']]

    for _, row in df_new_spotbugs_unmatch.iterrows():
        df_spotbugs_unmatch.loc[(df_spotbugs_unmatch.pattern == row['type']) & (df_spotbugs_unmatch.path == row['path']) & (df_spotbugs_unmatch.lineno == row['line no']), ['codeline', 'Is our FN?', "Is SP's FP?", 'Can we fix', 'Reason', 'label limitation(rbugs)', 'Note']] = [row['Codeline'], row['Is our FN?'], row["Is SP's FP?"], row['Can we fix'], row['Reason'], row['label limitation(rbugs)'], row['Note']]


mark_new()
auto_fill_new()

writer = pd.ExcelWriter('out.xlsx', engine='xlsxwriter')
df_match.to_excel(writer, sheet_name='matched', index=False)
df_rbugs_unmatch.to_excel(writer, sheet_name='rbugs-unmatched', index=False)
df_spotbugs_unmatch.to_excel(writer, sheet_name='spotbugs-unmatched', index=False)
writer.save()
# %%
