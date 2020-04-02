import pandas as pd
import json
from pandas.io.json import json_normalize
from pathlib import Path


Path('dist').mkdir(parents=True, exist_ok=True)

languages = ['en', 'trr']
header = ['English', 'Turkish'] 

data_list = []
for lang in languages:
    fpath = '{}.json'.format(lang)
    if Path(fpath).is_file():
        with open(fpath, 'r') as f:
            data = json.load(f)
            data_list.append(data)
    else:
        data_list.append(dict())


df = json_normalize(data_list)

# print(df.columns)

df2 = df.transpose()
df2.to_csv('output.csv', header=header, index=True)




df3 = pd.read_csv("output.csv", index_col=0)

df4 = df3.transpose()
df4.reset_index(drop=True, inplace=True)

# df4.to_json("output.json", orient='records')
df4.fillna('', inplace=True)

for i,row in enumerate(df4.to_dict('r')):
    tmp_dict = {}
    for key,val in row.items():
        if '.' in key:
            key1,key2 = key.split('.')
            if not tmp_dict.get(key1): tmp_dict[key1] = {}
            tmp_dict[key1][key2] = val
        else:
            tmp_dict[key] = val
            
    with open('dist/{}_out.json'.format(languages[i]), 'w') as f:
        json.dump(tmp_dict, f)



aa=0