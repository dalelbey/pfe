from google_play_scraper import Sort, reviews, app
import json
import numpy as np
import pandas as pd

from datetime import datetime,date

def size(s: str, default_val: int) -> int:
    x: int
    if s[-1] == 'k':
        x = int(float(s[:-1]) * 1_000)
    elif s[-1] == 'M':
        x = int(float(s[:-1]) * 1_000_000)
    else:
        x = default_val
    return x

search = 'com.facebook.lite'
app_infos = []
info = app(search, lang='en')
del info['comments']
app_infos.append(info)
    #print(app_infos)
    


    #print_json(app_infos[0])
data = pd.DataFrame(app_infos)
print(data)
title = data['title'][0]
    
installs = data['installs'].values
score = data['score']
reviews = data['reviews']
ratings = data['ratings']
released = data['released']
genre = data['genre']
print(title)

context = {
        'title' : title, 'installs' : installs, 'score' : score, 'reviews' : reviews, 'ratings' : ratings, 'released' :  released, 'genre' : genre

     }

