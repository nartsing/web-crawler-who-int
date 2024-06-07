import os 
import json
import base64
import tqdm

files=os.listdir("./data")

datas=[]

for file in files:
    datas+=json.load(open("./data/"+file))

out={

}


for item in tqdm.tqdm(datas):
    if "msg" in item:
        continue
    data=item["data"]
    url=item["url"]
    if "message" in data:
        continue
    data=json.loads(data)
    '''
    indicator_country_year_age_sex:value
    '''
    # base64 解析url.split("=")[-1]
    parm=url.split("=")[-1]
    parm=base64.b64decode(parm).decode()
    parm=json.loads(parm)
    key_pre=f"{parm['dataFilters'][0]['values'][0]}_{parm['dataFilters'][1]['values'][0]}_{parm['dataFilters'][2]['values'][0]}"
    for j in data:
        key_1=j['name']
        for k in j['children']:
            key_2=k['name']
            value=k['value']
            key=key_pre+"_"+key_1+"_"+key_2
            out[key]=value
    
index=['indicator', 'country', 'year', 'age', 'sex', 'death_count']
lists=[]
for key in tqdm.tqdm(out):
    key_new=key.split("_")
    lists.append([key_new[0],key_new[1],key_new[2],key_new[3],key_new[4],out[key]])

with open("data.csv","w") as f:
    f.write(",".join(index))
    f.write("\n")
    for i in tqdm.tqdm(lists):
        f.write(",".join([str(j) for j in i]))
        f.write("\n")

print()
