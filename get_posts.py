import pandas as pd
import requests
import re




df_all = pd.DataFrame({'FILE':['zerokanna','kanna2']})
classes = pd.read_csv('classes.txt',header=None,names=['class'])
print(classes)
pat = "|".join(classes['class'])
print(pat)

def split_it(year):
    return re.findall(pat,year, re.IGNORECASE)

for mclass in classes['class']:
    #print(mclass)
    df_all[mclass] = df_all['FILE'].str.contains(mclass,regex=True,case=False)



print(df_all['Kanna'].count())


# pd.set_option('display.max_colwidth', -1)
# #pd.set_option('display.max_rows', -1)
r = requests.get('https://api.pushshift.io/reddit/search/submission', params= {'subreddit':'maplestory','sort':'desc','sort_type':'created_utc', 'after':1546329600,'before':1669881600,'size':100})
records =pd.read_json(r.text,orient='record')
records  =  records['data'].apply(pd.Series)
# print(r.json()['data'][0])
# print('--------------')
# print(records2.iloc[0]['wls'])

for mclass in classes['class']:
    #print(mclass)
    records[mclass] = records['title'].str.contains(mclass,regex=True,case=False)




totals  = pd.DataFrame(records.loc[:,classes['class']].sum(axis=0),columns=['count'])

totals.reset_index(level=0, inplace=True)

print(totals)


classes  = classes.set_index('class').join(totals.set_index('index')).reset_index()
classes.rename(columns={'index':'class'}, inplace=True)
print(classes)


