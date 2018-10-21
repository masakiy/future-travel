
# coding: utf-8

# In[4]:


from requests_oauthlib import OAuth1Session
import json
import re
import urllib
import subprocess
import settings
import time, calendar
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import io

import datetime
#subprocess.run(['jupyter', 'nbconvert', '--to', 'python', 'tweet_picture_get.ipynb'])
               
CK = settings.CONSUMER_KEY
CS = settings.CONSUMER_SECRET
AT = settings.ACCESS_TOKEN
ATS = settings.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS)

######入力情報
#出発地、時刻
dep_place='名古屋駅'
dep_time=8    #8時
#目的地、時刻
des_place='伊勢神宮'
des_time=11
#帰着地、時刻
ret_place='東京駅'
ret_time=20

# ツイッター上で出発地または目的地の入ったツイートを〇〇個取得する
def get_target_word(word):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {'q':word,
              'count':100
          }
    req = twitter.get(url, params = params)
    timeline = json.loads(req.text)
    return timeline

def YmdHMS(created_at):
    time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
    unix_time = calendar.timegm(time_utc)
    time_local = time.localtime(unix_time)
    return int(time.strftime("%Y%m%d%H%M%S", time_local))

# 取得したツイートに画像があれば、その画像を取得する
def get_illustration(timeline,key_time):
    global image
    global image_number
    image_number = 0
    image_get_flag = 0
    check_image = []
    loop_num = 0
    for tweet in timeline['statuses']:
        #検旅行での出発地、経由地、目的地の到着時刻と投稿時刻が近いtweetをフィルタリング。（±4時間） 
        loop_num  +=1
        if key_time -4 < int(str(YmdHMS(tweet['created_at']))[8:10]) < key_time +4:
            #画像があれば、画像とツイートを取得
            try:                
                media_list = tweet['extended_entities']['media']
#                #画像をarrayに変換
#                im_list = np.asarray(image)
#                #貼り付け
#                plt.imshow(im_list)
#                #表示
#                plt.show()
                    
                for media in media_list:
                    image = media['media_url']
                    check_image.append(image)
                    image_number += 1
                    image_get_flag = 1
                    
                    file =io.BytesIO(urllib.request.urlopen(image).read())
                    img = Image.open(file)
                    img.show()
                    
                    return img, tweet['text']       
                    break
    #        except KeyError:
    #            print("KeyError:画像を含んでいないツイートです")
    #        except:
    #            print("error")
            except:
                pass
        #条件を満たすtweetが見つからなかった時
        elif loop_num == len(timeline['statuses']) and image_get_flag == 0:
            #適当な画像とコメントを表示
            image='https://1.bp.blogspot.com/-ZsRZh52shXU/WWNBGGNeLjI/AAAAAAABFZg/rRxw5r719Jk_ymwSq7sViPCl0DIcHjXigCLcBGAs/s600/travel_happy_family_set.png'
            file =io.BytesIO(urllib.request.urlopen(image).read())
            img = Image.open(file)
            img.show()
            return img,'旅行楽しい！'
#            pass            
        else:
            pass            


if __name__ == '__main__':
    # 検索対象の単語を設定
    # ORで条件を付けれる
    # 例:word = "ラーメン+OR+伊勢神宮"
    # ならば、ツイートに出発地または目的地含まれる物を取得

    print('----------------------------------------------------')
    #出発地、時間
    keyword_dep = dep_place + '行'
    print(keyword_dep, dep_time,'時')
    timeline = get_target_word(keyword_dep)
    #画像と感想を出力
    illust_img_dep, illust_text_dep = get_illustration(timeline,dep_time)    
    print(illust_img_dep, illust_text_dep)
    
    print('----------------------------------------------------')
    #目的地、時間
    keyword_des = des_place
    print(keyword_des, des_time,'時')
    timeline = get_target_word(keyword_des)
    #画像と感想を出力
    illust_img_des,illust_text_des =  get_illustration(timeline,des_time)    
    print(illust_img_des, illust_text_des)
    print('----------------------------------------------------')
    #帰着地、時間
    keyword_ret = ret_place + '帰'
    print(keyword_ret, ret_time,'時')
    timeline = get_target_word(keyword_ret)
    #画像と感想を出力
    illust_img_ret,illust_text_ret = get_illustration(timeline,ret_time)    
    print(illust_img_ret, illust_text_ret)
    print('----------------------------------------------------')

