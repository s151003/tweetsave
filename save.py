import configparser
from twitter import *
import json
import urllib.request
from tweetsave import api 

def auth():
    ini = configparser.ConfigParser()
    ini.read('./keys.ini','UTF-8')

    CK = ini.get('Keys','Consumer_Key')
    CS = ini.get('Keys','Consumer_Secret')
    AT = ini.get('Keys','Access_Token')
    ATS = ini.get('Keys','Access_Token_Secret')
    t = Twitter(auth=OAuth(AT,ATS,CK,CS))
    return t
t = auth()

def get_timeline(screen_name,max=None):
    try:
        if max:
            return t.statuses.user_timeline(screen_name=screen_name,max_id=max,count="200")
        else:
            return t.statuses.user_timeline(screen_name=screen_name,count="200")
    except:
        print("Twitter API取得制限 15分後に再実行")
        
def savetweets(tweets):
    max=""
    l = len(tweets)
    for i in range(0,l):
        response = api.save(str(tweets[i]['id']))
        print(response['status'],response['message'])
        print(tweets[i]['id'])
        if i == l:
            max=tweets[i]['id']
    return max

def main():
    tweets=get_timeline("muratamika2020")
    max = savetweets(tweets)
    for i in range(0,4):
        tweets= get_timeline("muratamika2020",max)
        max = savetweets(tweets)

main()