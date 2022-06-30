"""
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
def redirect(request):
    return HttpResponseRedirect('home')

def index(request):
    if request.user.is_authenticated:
        return render(request , 'index.html')
    else:
        return  HttpResponseRedirect('dashborad/login')

def login(request):
    if request.user.is_authenticated:
         return HttpResponseRedirect('/dashborad')
    else:
        return render(request , 'user/login.html')  
"""   
import chunk
from collections import UserString
from gettext import install
from importlib.resources import path
from multiprocessing import context
###
import os
from urllib import response
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import mimetypes
##
from site import USER_BASE
from turtle import title
from unicodedata import category
from django.http import JsonResponse
from django.shortcuts import render, redirect
from requests import session
from .models import Download, Message , Admin, Recherche
#pdf
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
#pdf
#from dashboard.models import Order
from django.core import serializers
from django.contrib.auth.models import User

from ftplib import all_errors
from os import link
import time
from h11 import InformationalResponse
from selenium import webdriver
import csv

#google_play_scraper
from google_play_scraper import Sort, reviews, app
import json
import pandas as pd
import numpy as np
from datetime import datetime,date

from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
import nltk

from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm import tqdm
from tqdm.notebook import tqdm
"""
def dashboard_with_pivot(request):
    return render(request, 'dashboard_with_pivot.html', {}) #fonction qui dirige un utilisateur vers les modèles spécifiques définis dans le dashboard/templates

def pivot_data(request):
    dataset = Order.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False) #méthode auxiliaire qui envoie la réponse avec les données au tableau croisé dynamique sur le front-end de l'application.
"""


def index(request):

    data = pd.read_csv("C:\\Users\\ACER\\Downloads\\googleplaystore.csv\\googleplaystore.csv")
    data.drop_duplicates(inplace=True)
    data.dropna(inplace=True)
    data['Reviews'] = data['Reviews'].astype('int')

    data['Size'] = data['Size'].apply(lambda s: size(s, 9_400_000))

    columns = ['Installs', 'Price']
    for col in columns:
       data[col] = pd.to_numeric(data[col].replace(r'\D', '', regex=True))

    columns = ['Current Ver', 'Android Ver']
    
    
    for col in columns:
        data[col] = pd.to_numeric(data[col].str.replace(r'[a-zA-Z]', '', regex=True)\
                                .str.strip(), errors='ignore')\
                                .replace('', np.nan)
    
    last_date = pd.to_datetime(data['Last Updated'])
    data['Last Updated days ago'] = last_date.apply(lambda x: date.today() - datetime.date(x))

    data.drop("Last Updated", inplace=True, axis=1)
    dt = data.groupby(['Category'])[['Price', 'Installs']].agg('sum').sort_values(by='Installs', ascending=False)

    Category = dt.groupby(['Category'])[['Price', 'Installs']].agg('sum')\
                    .sort_values(by='Installs', ascending=False)\
                    .index.get_level_values('Category')\
                    .to_list()
                        

    
    

    Installs = dt['Installs'].to_list()
    Price = dt['Price'].to_list()
    count = data['Type'].value_counts()
    count_list = [c for c in count]
    
    context = {"Category":Category,"Installs":Installs,"Price":Price,"count_list":count_list}
    
    request.session['context'] = 'context'
    
    return render(request, 'dashboard/index.html', context)

#----------
def size(s: str, default_val: int) -> int:
    x: int
    if s[-1] == 'k':
        x = int(float(s[:-1]) * 1_000)
    elif s[-1] == 'M':
        x = int(float(s[:-1]) * 1_000_000)
    else:
        x = default_val
    return x

def index1(request):
    return redirect(request,index)

def app_profil(request):
    search = 'com.facebook.lite' 
    app_infos = []
    info = app(search, lang='en')
    del info['comments']
    app_infos.append(info)
    title = app_infos[0]['title']
    icon = app_infos[0]['icon']
    screenshots = app_infos[0]['screenshots']
    for i in range(len(screenshots)):
     screenshots[i]
     
    s1 = screenshots[0]
    s2 = screenshots[1]
    s3 = screenshots[2]
    print_json(app_infos[0])
    app_reviews = []
    for score in list(range(1, 6)):
      for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
        rvs, _ = reviews(
          search,
          lang='en',
          country='us',
          sort=sort_order,
          count= 200 if score == 3 else 100,
          filter_score_with=score
        )
        for r in rvs:
          r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
          r['appId'] = search
        app_reviews.extend(rvs)

    app_reviews_df = pd.DataFrame(app_reviews)
    app_reviews_df.to_csv(r'Files\facebookreviews.csv', index=None, header=True)
    
    app_reviews_df['at']

    for i in range(len(app_reviews_df['at'])):
        app_reviews_df['at'][i] = str(app_reviews_df['at'][i]).split(' ')[0]
    date = app_reviews_df['at']
    date
    value_counts = app_reviews_df['at'].value_counts().sort_index()
    app_reviews_df
    value_counts_after = []
    index_counts_after = []
    for element in list(value_counts.keys()):
        value = str(element).split(' ')[0]
        value_counts_after.append(value)
    print(value_counts)
    print(value_counts_after)

    for i in value_counts:
        index_counts_after.append(i)
    print(index_counts_after)

    context = {
        'value_counts_after' : value_counts_after, 'index_counts_after' : index_counts_after, 'title' : title, 'icon' : icon, 's1' : s1, 's2' : s2, 's3' : s3
     }

   
    return render(request, 'dashboard/app_profil.html', context)


def search_history(request):
    user = User.objects.get(pk=request.session['user_id'])
    #nom = request.session['user_id'].get_username()

    liste_recherches =  Recherche.objects.filter(user = user)

    return render(request, 'dashboard/search_history.html', {'liste_recherches':liste_recherches})



def download(request):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename = request.POST['filename']
    filepath = base_dir + '/Files/' + filename
    thefile = filepath
    filename = os.path.basename(thefile)
    chunk_size = 8192
    #filename='%s.csv'%(filename)
    response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size),
                        content_type  = 'text/csv', headers={'Content-Disposition': f'attachment; filename="{filename}"'})
    
    user = User.objects.get(pk=request.session['user_id'])
    download = Download.objects.create(file_name=filename , user = user)
    download.save()

    #response['Content_Length'] = os.path.getsize(thefile)
    #response['Content_Disposition'] = "attachment;filename=%s" % filename
    return response


def export_pdf(request):
    search ='com.facebook.lite'
    
    app_infos = []
    info = app(search, lang='en')
    del info['comments']
    app_infos.append(info)
    #print(app_infos)
    


    #print_json(app_infos[0])
    data = pd.DataFrame(app_infos)
    data.to_csv(r'Files\appinformation.csv', index=None, header=True)
    print(data)
    title = data['title'][0]#.values[0]
    installs = data['installs'][0]
    score = data['score'][0]
    reviews = data['reviews'][0]
    ratings = data['ratings'][0]
    released = data['released'][0]
    genre = data['genre'][0]
    icon = data['icon'][0]
    template_path = 'dashboard/pdf_output.html'
    context = {
        'title' : title, 'installs' : installs, 'score' : score, 'reviews' : reviews, 'ratings' : ratings, 'released' :  released, 'genre' : genre, 'icon' : icon

     }
    
    
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="appinformation.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    
    return render(request, "dashboard/export_pdf.html")


def download_history(request):
    user = User.objects.get(pk=request.session['user_id'])
    liste_downloads =  Download.objects.filter(user = user)
    return render(request, "dashboard/download_history.html", {'liste_downloads':liste_downloads})


def review_analysis(request):
    search = 'com.yoinsapp' 
    app_infos = []
    info = app(search, lang='en')
    del info['comments']
    app_infos.append(info)
    title = app_infos[0]['title']
    icon = app_infos[0]['icon']
    print_json(app_infos[0])
    app_reviews = []
    for score in list(range(1, 6)):
      for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
        rvs, _ = reviews(
          search,
          lang='en',
          country='us',
          sort=sort_order,
          count= 200 if score == 3 else 100,
          filter_score_with=score
        )
        for r in rvs:
          r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
          r['appId'] = search
      app_reviews.extend(rvs)

    app_reviews_df = pd.DataFrame(app_reviews)
    app_reviews_df.to_csv(r'Files\reviewsyonisapp.csv', index=None, header=True)
   
    
    dt = app_reviews_df['score'].value_counts().sort_index()
    dt1 = pd.DataFrame(dt)
   # dt1.to_csv(r'Files\yonisreviewstarby.csv', index=None, header=True)
    ax = []
    x1 = dt1.values[0][0]
    x2 = dt1.values[1][0]
    x3 = dt1.values[2][0]
    x4 = dt1.values[3][0]
    x5 = dt1.values[4][0]
    ax = [x1,x2,x3,x4,x5]
    ay =[]
    y1 = dt1.index[0]
    y2 = dt1.index[1]
    y3 = dt1.index[2]
    y4 = dt1.index[3]
    y5 = dt1.index[4]
    ay = [y1,y2,y3,y4,y5]

    review1 = app_reviews_df['content'][0]
    review2 = app_reviews_df['content'][1]
    review3 = app_reviews_df['content'][2]

    userName1 = app_reviews_df['userName'][0]
    userName2 = app_reviews_df['userName'][1]
    userName3 = app_reviews_df['userName'][2]

    userImage1 = app_reviews_df['userImage'][0]
    userImage2 = app_reviews_df['userImage'][1]
    userImage3 = app_reviews_df['userImage'][2]

    at1 = app_reviews_df['at'][0]
    at2 = app_reviews_df['at'][1]
    at3 = app_reviews_df['at'][2]
    

    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    
    res = {}
    for i, row in tqdm(app_reviews_df.iterrows(), total=len(app_reviews_df)):
       content = row['content']
       reviewId = row['reviewId']
       res[reviewId	] = sia.polarity_scores(content)

    pos = 0
    neg = 0
    neu = 0

    vaders = pd.DataFrame(res).T
    vaders.to_csv(r'Files\review_analyss_yonisapp.csv', index=None, header=True)
    vaders = vaders.reset_index().rename(columns={'index': 'reviewId'})
    vaders = vaders.merge(app_reviews_df, how='left')
    
    for i in range(len(app_reviews)):
         pos = pos + vaders['pos'][i] 
         neg = neg + vaders['neg'][i]
         neu = neu + vaders['neu'][i]
  
    pos = round((pos/ len(app_reviews)), 2)
    neg = round((neg/ len(app_reviews)), 2)
    neu = round((neu/ len(app_reviews)), 2)


    context = {
        'ax' : ax, 'ay' : ay, 'pos' : pos, 'neg' : neg, 'neu' : neu, 'review1' : review1, 'review2' : review2, 'review3' : review3, 'userName1' : userName1, 'userName2' : userName2, 'userName3' : userName3, 'userImage1' : userImage1, 'userImage2' : userImage2, 'userImage3' : userImage3, 'at1' : at1, 'at2' : at2, 'at3' : at3, 'title' : title, 'icon' : icon
     }

    
    return render(request, "dashboard/review_analysis.html", context)


def searchprofil(request):
    search = request.GET['search'] 
    app_infos = []
    info = app(search, lang='en')
    del info['comments']
    app_infos.append(info)
    title = app_infos[0]['title']
    icon = app_infos[0]['icon']
    screenshots = app_infos[0]['screenshots']
    for i in range(len(screenshots)):
     screenshots[i]
     
    s1 = screenshots[0]
    s2 = screenshots[1]
    s3 = screenshots[2]
    print_json(app_infos[0])
    app_reviews = []
    for score in list(range(1, 6)):
      for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
        rvs, _ = reviews(
          search,
          lang='en',
          country='us',
          sort=sort_order,
          count= 200 if score == 3 else 100,
          filter_score_with=score
        )
        for r in rvs:
          r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
          r['appId'] = search
        app_reviews.extend(rvs)

    app_reviews_df = pd.DataFrame(app_reviews)
    app_reviews_df.to_csv(r'Files\reviews.csv', index=None, header=True)
    app_reviews_df['at']

    for i in range(len(app_reviews_df['at'])):
        app_reviews_df['at'][i] = str(app_reviews_df['at'][i]).split(' ')[0]
    date = app_reviews_df['at']
    date
    value_counts = app_reviews_df['at'].value_counts().sort_index()
    app_reviews_df
    value_counts_after = []
    index_counts_after = []
    for element in list(value_counts.keys()):
        value = str(element).split(' ')[0]
        value_counts_after.append(value)
    print(value_counts)
    df = pd.DataFrame(value_counts)
    df.to_csv(r'Files\scorebystar.csv', index=None, header=True)
    print(value_counts_after)

    for i in value_counts:
        index_counts_after.append(i)
    print(index_counts_after)

    context = {
        'value_counts_after' : value_counts_after, 'index_counts_after' : index_counts_after, 'title' : title, 'icon' : icon, 's1' : s1, 's2' : s2, 's3' : s3
     }


    user = User.objects.get(pk=request.session['user_id'])
    #nom = request.session['user_id'].get_username()

    recherche = Recherche.objects.create(url= search, user = user)
    recherche.save()
    

    return render(request, "dashboard/searchprofil.html", context)




def searchreview(request):
    search = request.GET['search'] 
    app_infos = []
    info = app(search, lang='en')
    del info['comments']
    app_infos.append(info)
    title = app_infos[0]['title']
    icon = app_infos[0]['icon']
    print_json(app_infos[0])
    app_reviews = []
    for score in list(range(1, 6)):
      for sort_order in [Sort.MOST_RELEVANT, Sort.NEWEST]:
        rvs, _ = reviews(
          search,
          lang='en',
          country='us',
          sort=sort_order,
          count= 200 if score == 3 else 100,
          filter_score_with=score
        )
        for r in rvs:
          r['sortOrder'] = 'most_relevant' if sort_order == Sort.MOST_RELEVANT else 'newest'
          r['appId'] = search
      app_reviews.extend(rvs)

    app_reviews_df = pd.DataFrame(app_reviews)
    app_reviews_df.to_csv('reviews.csv', index=None, header=True)
   
    
    dt = app_reviews_df['score'].value_counts().sort_index()
    dt1 = pd.DataFrame(dt)
    ax = []
    x1 = dt1.values[0][0]
    x2 = dt1.values[1][0]
    x3 = dt1.values[2][0]
    x4 = dt1.values[3][0]
    x5 = dt1.values[4][0]
    ax = [x1,x2,x3,x4,x5]
    ay =[]
    y1 = dt1.index[0]
    y2 = dt1.index[1]
    y3 = dt1.index[2]
    y4 = dt1.index[3]
    y5 = dt1.index[4]
    ay = [y1,y2,y3,y4,y5]

    review1 = app_reviews_df['content'][0]
    review2 = app_reviews_df['content'][1]
    review3 = app_reviews_df['content'][2]

    userName1 = app_reviews_df['userName'][0]
    userName2 = app_reviews_df['userName'][1]
    userName3 = app_reviews_df['userName'][2]

    userImage1 = app_reviews_df['userImage'][0]
    userImage2 = app_reviews_df['userImage'][1]
    userImage3 = app_reviews_df['userImage'][2]

    at1 = app_reviews_df['at'][0]
    at2 = app_reviews_df['at'][1]
    at3 = app_reviews_df['at'][2]
    

    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    
    res = {}
    for i, row in tqdm(app_reviews_df.iterrows(), total=len(app_reviews_df)):
       content = row['content']
       reviewId = row['reviewId']
       res[reviewId	] = sia.polarity_scores(content)

    pos = 0
    neg = 0
    neu = 0

    vaders = pd.DataFrame(res).T
    vaders.to_csv(r'Files\review_analyss.csv', index=None, header=True)
    vaders = vaders.reset_index().rename(columns={'index': 'reviewId'})
    vaders = vaders.merge(app_reviews_df, how='left')

    for i in range(len(app_reviews)):
         pos = pos + vaders['pos'][i] 
         neg = neg + vaders['neg'][i]
         neu = neu + vaders['neu'][i]
  
    pos = round((pos/ len(app_reviews)), 2)
    neg = round((neg/ len(app_reviews)), 2)
    neu = round((neu/ len(app_reviews)), 2)


    context = {
        'ax' : ax, 'ay' : ay, 'pos' : pos, 'neg' : neg, 'neu' : neu, 'review1' : review1, 'review2' : review2, 'review3' : review3, 'userName1' : userName1, 'userName2' : userName2, 'userName3' : userName3, 'userImage1' : userImage1, 'userImage2' : userImage2, 'userImage3' : userImage3, 'at1' : at1, 'at2' : at2, 'at3' : at3, 'title' : title, 'icon' : icon
     }
     


    user = User.objects.get(pk=request.session['user_id'])
    #nom = request.session['user_id'].get_username()

    recherche = Recherche.objects.create(url= search, user = user)
    recherche.save()
    
    return render(request, "dashboard/searchreview.html", context)



def categorie(request):
    data = pd.read_csv("C:\\Users\\ACER\\Downloads\\googleplaystore.csv\\googleplaystore.csv")
    app_category=[]
    Categorie = request.GET['Categorie'] 
    for i in range(len(data)):
        app = {}
        if(data['Category'][i] == Categorie):

            app['App'] = data['App'][i]
            app['Category'] = data['Category'][i]
            app['Installs'] = data['Installs'][i]
            app['Price'] = data['Price'][i]
            app['AndroidVer'] = data['Android Ver'][i]
            app['Reviews'] = data['Reviews'][i]
            app['Size'] = data['Size'][i]
            app['Type'] = data['Type'][i]
            app_category.append(app)
    n = range(len(app_category))
    zipped = zip(n, app_category)
    context={"zipped" : zipped,}

    return render(request, "dashboard/categorie.html", context)

def form_basic(request):
    return render(request, "dashboard/form_basic.html")




def form_wizard(request):
    return render(request, "dashboard/form_wizard.html")




def smilar_app(request):
    
    return render(request, "dashboard/smilar_app.html")




def icon_material(request):
    return render(request, "dashboard/icon-material.html")




def icon_fontawesome(request):
    return render(request, "dashboard/icon-fontawesome.html")




def new_app(request):
    return render(request, "dashboard/new_app.html")




def gallery(request):
    return render(request, "dashboard/gallery.html")





def invoice(request):
    return render(request, "dashboard/invoice.html")



def chat(request):
    return render(request, "dashboard/chat.html")

def print_json(json_object):
  json_str = json.dumps(
    json_object,
    indent=2,
    sort_keys=True,
    default=str
  )
  print(highlight(json_str, JsonLexer(), TerminalFormatter()))

def search(request):
    search = request.GET['search']
    
    app_infos = []
    info = app(search, lang='en')
    del info['comments']
    app_infos.append(info)
    #print(app_infos)
    


    #print_json(app_infos[0])
    data = pd.DataFrame(app_infos)
    data.to_csv(r'Files\appinformation.csv', index=None, header=True)
    print(data)
    title = data['title'][0]#.values[0]
    installs = data['installs'][0]
    score = data['score'][0]
    reviews = data['reviews'][0]
    ratings = data['ratings'][0]
    released = data['released'][0]
    genre = data['genre'][0]
    icon = data['icon'][0]
    context = {
        'title' : title, 'installs' : installs, 'score' : score, 'reviews' : reviews, 'ratings' : ratings, 'released' :  released, 'genre' : genre, 'icon' : icon

     }
    
    user = User.objects.get(pk=request.session['user_id'])
    #nom = request.session['user_id'].get_username()

    recherche = Recherche.objects.create(url= search, user = user, title= data['title'][0])
    recherche.save()
    return render(request, 'dashboard/search.html', context)





"""
    information = []
    data={}
    data['title'] = title
    data['installs'] = installs
    data['score'] = score
    data['reviews'] = reviews
    data['ratings'] = ratings
    data['released'] = released
    data['genre'] = genre
    
    
      #driver.find_element_by_xpath("//h1[contains(@class,'Fd93Bb F5UCq p5VxAd')]").text 
      #data['app_name'] = driver.find_element_by_tag_name("h5").text
    information.append(data)
      #print(review)

    
    context = {
        'information' : information

     }
    

   


   #data = pd.DataFrame(list_all_new_app,columns=['Name', 'nbretoiles', 'nbrreview', 'Taille', 'Installs', 'Email Address'])
   # data.to_csv('scraping_playstore.csv', header = True, index=False)       
"""
    

