# coding: UTF-8
from requests_oauthlib import OAuth1Session
from time import sleep
import json
import urllib.request
import sqlite3

def twitter_auth():
 KEYS = { # 自分のアカウントで入手したキーを下記に記載
        'consumer_key':'######',
        'consumer_secret':'#####',
        'access_token':'######',
        'access_secret':'#####',
       }
  #Oauthで上記のキーを通す
 twitter = OAuth1Session(KEYS['consumer_key'], KEYS['consumer_secret'], KEYS['access_token'], KEYS['access_secret'])
 return  twitter


def twitter_get(twitter,max):
 max_id = max
 url = "https://api.twitter.com/1.1/favorites/list.json"
 params = {'count': 200,'max_id':max_id}
 request = twitter.get(url, params=params)
 favorites = json.loads(request.text)
 return favorites


def image_seve(favorites):
    for i, fav in enumerate(favorites):
     try:
        if fav['extended_entities']['media']is not None:
         length = len(fav['extended_entities']['media'])
         print(i,fav['user']['name'],"@ "+fav['user']['screen_name'])
         for count  in range(length):
          if fav['extended_entities']['media'][count] is not None:
              url    = fav['extended_entities']['media'][count]['media_url_https']
              url_large = url+ ":large"#twitterの画像を大きいサイズで表示
              slice_url = url[28:]#URLから元ファイル名を取得
              urllib.request.urlretrieve(url_large, "@"+fav['user']['screen_name']+"_"+slice_url)
              max_id = fav['id'] - 1
     except KeyError:
         print("画像が含まれていないツイートです")
         max_id = fav['id'] - 1
    return max_id

if __name__ == "__main__":
    max_id  = None
    max     = None
    for i in range(15):
        twitter = twitter_auth()
        fav= twitter_get(twitter,max)
        max = image_seve(fav)
        twitter_get(twitter,max)






