#!/usr/bin/python

import sys
import tarfile
import json
import gzip
import pandas as pd
import botometer
from pandas.io.json import json_normalize

## VARIABLE INITIATION
#system argument
# arg 1 = 'rs' or 'sn'
# arg 2 = hour file 6,7 or 8 ?
# arg 3 = start row
# arg 4 = end row
# arg 5 = key selection, 1,2,3,4
# sn 7 : total row 33277
# sn 8 : total row 53310
# rs 7 : 7230
# rs 8 : 10493

mashape_key = "QRraJnMT9KmshkpJ7iu74xKFN1jtp1IyBBijsnS5NGbEuwIX54"

if(int(sys.argv[5])==1):
    twitter_app_auth = {
        'consumer_key': 'qngvt8PPer3irSHHkx71gqpJg',
        'consumer_secret': 'bAH258rRds9uWAi38kSwxgbJ1x0rAspasQACgOruuK4qnKsXld',
        'access_token': '218041595-yrk9WyMnTjh4PBidhApb0DwryK83Wzr32IWi6bP4',
        'access_token_secret': 'GCmOzFmzrOoAv59lCpKRQrC9e7H1P0449iaBW1rI66saS',
      }
elif (int(sys.argv[5])==2):
    twitter_app_auth = {
        'consumer_key': 'xQkTg8KSU7HlEEvaD8EJA',
        'consumer_secret': 'TMFRBmvGdGJtzwFJ3fyluPWszl5qCDuwBUqy0AGj0g',
        'access_token': '218041595-JUmLw0xEtnJVrqn03DCirlZpnL1Z7taWwKYZYUPN',
        'access_token_secret': 'cIdkjvTghunH6GGLRIjQW06ghyOFkX1w7jnurcJPVyIQw',
      }
elif (int(sys.argv[5])==3):
    twitter_app_auth = {
        'consumer_key': 'sPzHpcj4jMital75nY7dfd4zn',
        'consumer_secret': 'rTGm68zdNmLvnTc22cBoFg4eVMf3jLVDSQLOwSqE9lXbVWLweI',
        'access_token': '4258226113-4UnHbbbxoRPz10thy70q9MtEk9xXfJGOpAY12KW',
        'access_token_secret': '549HdasMEW0q2uV05S5s4Uj5SdCeEWT8dNdLNPiAeeWoX',
      }
elif (int(sys.argv[5])==4):
    twitter_app_auth = {
        'consumer_key': 'wZnIRW0aMRmHuQ3Rh5c2v7al4',
        'consumer_secret': 'ugFcKDc0WP7ktDw3Ch1ZddWknckkfFiH9ZvIKFDwg7k8ivDyFB',
        'access_token': '218041595-JSRBUY3CJ55km9Jb0QnJA6lQnyRoPfvpq6lNAsak',
        'access_token_secret': 'ck1wTLfMP5CeLAfnbkS3U7oKxY6e0xu9C7fosq3fNH8gO',
      }
else:
    twitter_app_auth = {
        'consumer_key': 'kcnlkVFRADdxaWNtWNAy3LquT',
        'consumer_secret': 'bAH258rRds9uWAi38kSwxgbJ1x0rAspasQACgOruuK4qnKsXld',
        'access_token': '218041595-yrk9WyMnTjh4PBidhApb0DwryK83Wzr32IWi6bP4',
        'access_token_secret': 'GCmOzFmzrOoAv59lCpKRQrC9e7H1P0449iaBW1rI66saS',
      }


bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)

if(sys.argv[1]=='rs'):
    input_file="data/distinct_userlist_rs_201606230"+sys.argv[2]+".csv"
else:
    input_file="data/distinct_userlist_201606230"+sys.argv[2]+".csv"
    
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

output_file="data/outputbot_201606230"+sys.argv[2]+"_"+sys.argv[1]+"_"+sys.argv[6]+".csv"
output_bot.to_csv(output_file, sep=',', encoding='utf-8')
