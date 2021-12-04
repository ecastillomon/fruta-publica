import pandas as pd
import numpy as np

df=pd.read_csv('data/Fruta publica/WhatsApp Chat with Fruta pública.txt',sep='\n', engine='python',header=None)
df['date_str']=df[0].apply(lambda x: re.findall('\d+/\d+/\d+, \d+:\d+ [AMP]{2}',x)).apply(lambda x: x[0] if len(x)>0 else None)
df['date']=df['date_str'].apply(lambda x: pd.to_datetime(x,format='%m/%d/%y, %H:%M %p', errors='ignore'))

df['user']=df[0].apply(lambda x: re.findall('-.*?:',x)).apply(lambda x: re.sub('- |:$','',x[0]) if len(x)>0 else None)
df['text']=df[0].apply(lambda x: re.sub('\d+/\d+/\d+.*-.*?:','',x))
df['location']=df[0].apply(lambda x: re.findall('[0-9.]+,[-]?[0-9.]+',x)).apply(lambda x: x[0] if len(x)>0 else None)
df['image']=df[0].apply(lambda x:re.findall('IMG.*\.jpg',x)).apply(lambda x: x[0] if len(x)>0 else None)
df['date']=df['date'].ffill()
df=df.drop(columns=0)
df['location']=df.groupby(['user','date'], as_index=True)['location'].transform(lambda x: x.ffill().bfill())
df['image']=df.groupby(['user','date'], as_index=True)['image'].transform(lambda x: x.ffill().bfill())
df['text']=df.groupby(['user','date'], as_index=True)['text'].transform(lambda x: ' '.join(x))
df['is_fruit']=df['text'].apply(lambda x: bool(re.search('IMG',x)) and bool(re.search('location:',x))  if type(x)==str else False)
df['inferred_fruit']=df['text'].apply(lambda x: re.sub('IMG.*?\.jpg \(file attached\)|location: .*[0-9.]+,[-]?[0-9.]+','',x)if type(x)==str else False)
df_temp=df.query('is_fruit').drop_duplicates()
df_temp.to_csv('temp.csv',index=False)

