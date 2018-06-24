import configparser
from twitter import *
from tweetsave import api 
from time import sleep

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
        sleep(60*15)
        get_timeline(screen_name,max=None)

def savetweets(tweets,turbo):
    max=""
    l = len(tweets)
    for i in range(0,l):
        response = api.save(str(tweets[i]['id']))
        print(response)
        print(tweets[i]['id'])
        if i == l:
            max=tweets[i]['id']
        if turbo != False:
            sleep(0.9)
    return max

def main():    
    ini = configparser.ConfigParser()
    ini.read('./keys.ini','UTF-8')
    screen_name = ini.get('save','user')
    turbo=ini.get('save','turbo')
    print("-----------------------")
    print("ユーザ名:",screen_name)
    if turbo:
        print("ターボモード:オン")
    else:
        print("ターボモード:オフ")
    print("-----------------------")
    tweets=get_timeline(screen_name)
    max = savetweets(tweets,turbo)
    for i in range(0,10):
        tweets= get_timeline(screen_name,max)
        max = savetweets(tweets,turbo)

main()