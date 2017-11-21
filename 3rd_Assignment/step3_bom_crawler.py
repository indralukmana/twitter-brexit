#!/usr/bin/python

import sys
import tarfile
import json
import gzip
import pandas as pd
import botometer
from pandas.io.json import json_normalize

## VARIABLE INITIATION

mashape_key = "QRraJnMT9KmshkpJ7iu74xKFN1jtp1IyBBijsnS5NGbEuwIX54"
twitter_app_auth = {
    'consumer_key': 'qngvt8PPer3irSHHkx71gqpJg',
    'consumer_secret': 'bAH258rRds9uWAi38kSwxgbJ1x0rAspasQACgOruuK4qnKsXld',
    'access_token': '218041595-yrk9WyMnTjh4PBidhApb0DwryK83Wzr32IWi6bP4',
    'access_token_secret': 'GCmOzFmzrOoAv59lCpKRQrC9e7H1P0449iaBW1rI66saS',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)

if(sys.argv[1]=='rs'):
    input_file="distinct_userlist_rs_201606230"+sys.argv[2]+".csv"
else:
    input_file="distinct_userlist_201606230"+sys.argv[2]+".csv"
    
bot_data = pd.read_csv(input_file, index_col = 0, names =['screen_name'])
print(len(bot_data))

distinct_uname=[]
for i in bot_data.values:
    distinct_uname.append((str('@'+i).replace("['","")).replace("']",''))


botoresult = pd.DataFrame()

for screen_name, result in bom.check_accounts_in(distinct_uname[int(sys.argv[3]):int(sys.argv[4])]):
    botoresult=botoresult.append(result, ignore_index=True)

output_bot=pd.concat([botoresult.user.apply(pd.Series), botoresult.scores.apply(pd.Series), botoresult.categories.apply(pd.Series)], axis=1)

print("bot result :",len(botoresult))
print("bot output :",len(output_bot))

output_file="outputbot_201606230"+sys.argv[2]+"_"+sys.argv[1]+"_"+sys.argv[3]+".csv"
output_bot.to_csv(output_file, sep=',', encoding='utf-8')
