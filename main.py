from flask import Flask, render_template, url_for, request
import pandas as pd
import numpy as np
from TMDBSEARCH import search as src
from ML import matlearn as mt
from Getnames import getname as gt
app = Flask(__name__)


@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response


@app.route('/')
def index():
    movies = getmovies()
    return render_template("index.html", movies=movies, actors=actorname, prod=productionname, director=directorname)


def getmovies():
    df = pd.read_csv("temp1.csv")
    a = df['Title']
    return a.values.tolist()


@app.route('/predict', methods=['POST'])
def predict():
    m = ''
    m = request.form['movie_name']
    m = m.split("~")
    if m[0] == 'movie':
       m=m[1]
       m=m.replace('&#39;',"'")
       res=mt.compute_cosine(m)
       k= src.get_data(list(res['Title']))
       data,er=src.get_data(m)
       cst=src.cast_dat(data['id'])
       direc1=src.direc(data['id'])
       a=src.get_comm(data['id'])
       gen=src.get_genres(data['id'])
       data=format_dat(er,data,k,cst,a,direc1,gen)
       movies=getmovies()
       return render_template("result.html" ,data=data ,l=list(res['Title']),movies=movies,actors=actorname,prod=productionname,director=directorname)
    if m[0]== 'actor':
        m=m[1]
        x=src.getactor_details(m)
        movies=getmovies()
        return render_template("actor.html",data=x,movies=movies,actors=actorname,prod=productionname,director=directorname)
    if m[0]== 'prod':
        m=m[1]
        x=src.get_prod(m)
        movies=getmovies()
        return render_template("prod.html",data=x,movies=movies,actors=actorname,prod=productionname,director=directorname)
    if m[0]=='dir':
        m=m[1]
        x=src.get_director(m)
        movies=getmovies()
        return render_template("director.html",data=x,movies=movies,actors=actorname,prod=productionname,director=directorname)
def format_dat(a,b,c,d,e,f,g):
    res={}
    res['d1']={}
    res['d3']={}
    res['d2']={}
    res['d4']={}
    res['d1']['title']=b['original_title']
    res['d1']['director']=f
    res['d1']['runtime']=120
    res['d1']['genres']=g
    res['d1']['desc']=b['overview']
    res['d1']['lang']=b['original_language']
    res['d1']['release_date']=b['release_date']
    res['d1']['production_comp']=a['production']
    res['d1']['cert']='Not_known'
    res['d1']['poster']="image/image_"+a['Title']+".png"
    res['d1']['vote_average']=b['vote_average']
    res['d1']['vote_count']=b['vote_count']
    for i in c.keys():
        poster_d="image/image_"+i+".png"
        res['d3'][i]={'title':i,'poster_p': poster_d , 'rating':c[i]['data']['vote_average'],'vote_count':c[i]['data']['vote_count']}
    for i in range(len(d)):
        res['d2'][i]={'name':d[i]['name'] ,'character':d[i]['character'],'bio' : d[i]['bio'],'popularity':d[i]['popularity'],'poster_p':d[i]['poster_p'],'dob':d[i]['dob']}
        if d[i]['gender']==1:
            res['d2'][i]['gender']='Female'
        elif d[i]['gender']==2:
            res['d2'][i]['gender']='Male'
        else:
            res[i]['d2'][i]['gender']='Other'
    for i in range(len(e)):
        pred = mt.Sim([e[i][1]])
        res['d4'][i]={'author':e[i][0],'review':e[i][1],'prediction':pred}
    return res

if __name__ == "__main__":
    df=pd.read_csv('temp1.csv')
    actorname=gt.get_actornames(df)
    directorname=gt.get_directornames(df)
    productionname=gt.get_productionnames(df)
    app.run(debug=True,port=8000) 

