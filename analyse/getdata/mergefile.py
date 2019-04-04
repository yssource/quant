import pandas as pd

file_set = ['IFH920181015@10', 'IFZ820181015@10']

df = pd.DataFrame()
for fs in file_set:
  temp_df = pd.read_csv(fs, sep=' ')
  df = df.append(temp_df)

df = df.sort_values(by=['time', 'ticker'])
merge_file_name = 'out.txt'
df.to_csv(merge_file_name, quoting=False, sep=' ', index=False)
