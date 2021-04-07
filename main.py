from flask import Flask,render_template,url_for,request
import pandas as pd
import numpy as np
from tmdbv3api import TMDb
import urllib.request
import json
import requests
tmdb = TMDb()
tmdb.api_key = 'ef83cac599a8b6b59be433cffe4aa715'
tmdb.language = 'en'
tmdb.debug = True
from tmdbv3api import Movie
movie = Movie()
url='https://api.themoviedb.org/3/search/movie?api_key=ef83cac599a8b6b59be433cffe4aa715&query='
poster_url='https://image.tmdb.org/t/p/original'
app=Flask(__name__)
@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():
    m=''
    m=request.form['movie_name']
    res=compute_cosine(m)
    k= get_data(list(res['Title']))
    data,er  =get_data(m)
    data=format_dat(er,data,k)
    return render_template("result.html" ,data=data ,l=list(res['Title']))
 
def get_data(m):
    if type(m)==list:
        k={}
        l={}
        for i in m:
            r=requests.get(url=url+i)
            r=r.json()
            lis = [(k, v) for k, v in r.items()]
            lis=lis[1][1][0]
            posterp=lis['poster_path']
            poster=requests.get(url=poster_url+posterp)
            poster=poster.content
            file = open("static/image/image_"+i+".png", "wb")
            file.write(poster)
            file.close()
            l['data']=lis
            l['poster']="static/image/image_"+i+".png"
            k[i]=l
        return k
    if type(m)==str:
        df=pd.read_csv("temp.csv") 
        a=df[df['Title']==m].values.tolist()
        c=df.columns
        c=np.column_stack((c,a[0])).tolist()
        del(c[9])
        r=requests.get(url=url+m)
        r=r.json()
        lis = [(k, v) for k, v in r.items()]
        lis=lis[1][1][0]   
        posterp=lis['poster_path']
        poster=requests.get(url=poster_url+posterp)
        poster=poster.content
        file = open("static/image/image_"+m+".png", "wb")
        file.write(poster)
        file.close()
        return lis,c

def format_dat(a,b,c):
    res={}
    res['d1']={}
    res['d3']={}
    res['d1']['title']=a[0][1]
    res['d1']['director']=a[3][1]
    res['d1']['runtime']=120
    res['d1']['desc']=b['overview']
    res['d1']['lang']=b['original_language']
    res['d1']['release_date']=b['release_date']
    res['d1']['production_comp']=a[4][1]
    res['d1']['cert']='Not_known'
    res['d1']['poster']="image/image_"+a[0][1]+".png"
    res['d1']['vote_average']=b['vote_average']
    res['d1']['vote_count']=b['vote_count']
    for i in c.keys():
        poster_d="image/image_"+i+".png"
        res['d3'][i]={'title':i,'poster_p': poster_d , 'rating':c[i]['data']['vote_average'],'vote_count':c[i]['data']['vote_count']}
    return res
def compute_cosine(a):
    df=pd.read_csv("temp1.csv")
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    c=CountVectorizer()
    i= pd.Series(df.index, index=df['Title'])
    ti=i[a]
    cm1=c.fit_transform(df['Attributes'])
    cosmi=cosine_similarity(cm1)
    cosmi=cosmi[ti]
    cosmi=list(enumerate(cosmi))
    cosmi=sorted(cosmi,key=(lambda i: i[1]),reverse=True)
    cosmi=cosmi[1:]
    mvs = [df['Title'][i[0]] for i in cosmi]  
    cosmi=pd.DataFrame(np.column_stack((cosmi,mvs)),columns=['Based Index','Score','Title'])    
    return cosmi[1:11]

if __name__ == "__main__":
    app.run(debug=True,port=8000) 

