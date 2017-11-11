#!/usr/bin/python

import sys
import tarfile
import json
import gzip
import pandas as pd
import botometer
from pandas.io.json import json_normalize

## VARIABLE INITIATION
tar = tarfile.open("../input/2017-09-22.tar.gz", "r:gz")
mashape_key = "QRraJnMT9KmshkpJ7iu74xKFN1jtp1IyBBijsnS5NGbEuwIX54"
twitter_app_auth = {
    'consumer_key': 'sPzHpcj4jMital75nY7dfd4zn',
    'consumer_secret': 'rTGm68zdNmLvnTc22cBoFg4eVMf3jLVDSQLOwSqE9lXbVWLweI',
    'access_token': '4258226113-4UnHbbbxoRPz10thy70q9MtEk9xXfJGOpAY12KW',
    'access_token_secret': '549HdasMEW0q2uV05S5s4Uj5SdCeEWT8dNdLNPiAeeWoX',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)
count = 0


# In[2]:

data = pd.DataFrame()
uname = pd.DataFrame()
count=0
#uname = []
for members in tar.getmembers():
    if (count==13):
        f = tar.extractfile(members)
        data = data.append(pd.read_json(f, lines=True))
        for memberx in data['user']:
            uname=uname.append(json_normalize(memberx)['screen_name'], ignore_index=True)
    count = count + 1


# In[4]:

len(uname)


# In[5]:

distinct_uname=[]
for i in uname.drop_duplicates().values:
    distinct_uname.append((str('@'+i).replace("[u'","")).replace("']",''))


# In[7]:

print("distinct uname",len(distinct_uname))
#asu=distinct_uname[0:180]


# In[ ]:

botoresult = pd.DataFrame()

for screen_name, result in bom.check_accounts_in(distinct_uname[int(sys.argv[2]):int(sys.argv[3])]):
    botoresult=botoresult.append(result, ignore_index=True)


# In[104]:

output_bot=pd.concat([botoresult.user.apply(pd.Series), botoresult.scores.apply(pd.Series), botoresult.categories.apply(pd.Series)], axis=1)


# In[103]:

print("bot result",len(botoresult))
print("bot output",len(output_bot))


# In[453]:
output_file="outputbot_"+sys.argv[1]+".csv"
output_bot.to_csv(output_file, sep=',', encoding='utf-8')

