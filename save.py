import configparser
from twitter import *
from tweetsave import api 
from time import sleep
import archiveis

def auth():
    ini = configparser.ConfigParser()
    ini.read('./config.ini','UTF-8')

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
    l = len(tweets)
    for i in range(0,l):
        id = tweets[i]['id_str']
        #print(archiveis.capture("https://twitter.com/Capitalnvest/status/"+id))
    
        response = api.save(id)
        print(response)
        if turbo == False:
            sleep(1)
    print(id)
    return id

def main():  
    ini = configparser.ConfigParser()
    ini.read('./config.ini','UTF-8')
    screen_name = ini.get('save','user')
    turbo=ini.get('save','turbo')
    if turbo == "True":
        turbo = True
    else:
        turbo = False
    if ini.get('save','max'):
        max = ini.get('save','max')
    else:
        max = None
    print("-----------------------")
    print("ユーザ名:",screen_name)
    if turbo:
        print("ターボモード:オン")
    else:
        print("ターボモード:オフ")
    print("-----------------------")
    
    for i in range(0,40):
        tweets= get_timeline(screen_name,max)
        max = savetweets(tweets,turbo)

main()