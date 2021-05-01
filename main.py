from flask import Flask, render_template, url_for, request
import pandas as pd
import numpy as np
from collections import Counter
import re
api_key='ef83cac599a8b6b59be433cffe4aa715'
url='https://api.themoviedb.org/3/search/movie?api_key=' +api_key+ '&query='
poster_url='https://image.tmdb.org/t/p/original'
import pandas as pd
import numpy as np
import json
import requests

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
       res=compute_cosine(m)
       k= get_data(list(res['Title']))
       data,er=get_data(m)
       cst=cast_dat(data['id'])
       direc1=direc(data['id'])
       a=get_comm(data['id'])
       gen=get_genres(data['id'])
       data=format_dat(er,data,k,cst,a,direc1,gen)
       movies=getmovies()
       return render_template("result.html" ,data=data ,l=list(res['Title']),movies=movies,actors=actorname,prod=productionname,director=directorname)
    if m[0]== 'actor':
        m=m[1]
        x=getactor_details(m)
        movies=getmovies()
        return render_template("actor.html",data=x,movies=movies,actors=actorname,prod=productionname,director=directorname)
    if m[0]== 'prod':
        m=m[1]
        x=get_prod(m)
        movies=getmovies()
        return render_template("prod.html",data=x,movies=movies,actors=actorname,prod=productionname,director=directorname)
    if m[0]=='dir':
        m=m[1]
        x=get_director(m)
        movies=getmovies()
        return render_template("director.html",data=x,movies=movies,actors=actorname,prod=productionname,director=directorname)

def compute_cosine(a):
    import pandas as pd
    df=pd.read_csv("temp1.csv")
    import numpy as np
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

def Sim(dat):
    import joblib as joblib
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.naive_bayes import MultinomialNB
    senti = open('sentiment_model.pkl','rb') 
    senti1 = joblib.load(senti)
    vect = open('cv.pkl','rb') 
    vect1 = joblib.load(vect)
    dat = vect1.transform(dat).toarray()
    pred = senti1.predict(dat)
    return pred
    
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
        pred = Sim([e[i][1]])
        res['d4'][i]={'author':e[i][0],'review':e[i][1],'prediction':pred}
    return res



def get_data(m):
    if type(m)==list:
        k={}
        for i in m:
            l={}
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
            k[i]=l
        return k
    if type(m)==str:
        df=pd.read_csv("temp1.csv") 
        a=df[df['Title']==m].values.tolist()
        c=df.columns
        c=np.column_stack((c,a[0])).tolist()
        del(c[9])
        c=dict(c)
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

def cast_dat(m):
    r='https://api.themoviedb.org/3/movie/'+str(m)+'/credits?api_key='+api_key+'&language=en-US'
    r=requests.get(url=r)
    r=r.json()
    r=r['cast']
    r=r[0:6]
    for i in r:
        a=getaddat(i['id'])
        i['bio']=a['bio']

        i['popularity']=a['popularity']
        i['poster_p']=cast_image(i['id'],i['name'])
        i['dob']=a['dob']
    return r
def direc(m):
    r='https://api.themoviedb.org/3/movie/'+str(m)+'/credits?api_key='+api_key+'&language=en-US'
    r=requests.get(url=r)
    r=r.json()
    r=r["crew"]
    for i in r:
        if (i['job']=='Director'):
            return i['name']
    
def getaddat(a):
    url='https://api.themoviedb.org/3/person/'+str(a)+'?api_key='+api_key+'&language=en-US'
    r=requests.get(url)
    r=r.json()
    r['biography']=r['biography'].replace('From Wikipedia, the free encyclopedia\n\n','')
    r['biography']=r['biography'].replace('\n\n',' ')
    return {'bio':r['biography'],'popularity':r['popularity'],'dob':r['birthday']}
def cast_image(m,n):
    url='https://api.themoviedb.org/3/person/'+str(m)+'/images?api_key='+api_key
    r=requests.get(url)
    r=r.json()
    r=r['profiles'][0]['file_path']
    poster=requests.get(url=poster_url+r)
    poster=poster.content
    n =n.replace('à', 'a')
    n=n.replace(' ','_')
    n=rem_uni(n)
    file = open("static/image_cast/"+n+".png", "wb")
    file.write(poster)
    file.close() 
    return "/image_cast/"+n+".png"

def rem_uni(a):
    a = a.replace('å','a')
    a = a.replace('á','a')   
    a = a.replace('é','e')
    a = a.replace('à','a')
    a = a.replace('è','e')
    a = a.replace('ù','u')
    a = a.replace('â','a')
    a = a.replace('ê','e')
    a = a.replace('î','i')
    a = a.replace('ô','o')
    a = a.replace('û','u')
    a = a.replace('ç','c')
    return a
def get_genres(m):
    r='https://api.themoviedb.org/3/movie/'+str(19995)+'?api_key='+api_key+'&language=en-US'
    r=requests.get(url=r)
    r=r.json()
    s=[]
    for i in r['genres']:
        s.append(i['name'])
    
    s = ["Sci-fi" if i=="Science Fiction" else i for i in s] 
    return s
def get_comm(a):
    url='https://api.themoviedb.org/3/movie/'+str(a)+'/reviews?api_key='+api_key+'&language=en-US&page=1'
    r=requests.get(url)
    r=r.json()
    r=r['results']
    a=[]
    for i in r:
        a.append([i['author'],i['content']])
    return a

def getactor_details(a):
    url='https://api.themoviedb.org/3/search/person/?api_key='+api_key+'&language=en-US&page=1&include_adult=false&query='+a
    r=requests.get(url=url)
    r=r.json()
    lis = [(k, v) for k, v in r.items()]
    lis=lis[1][1][0]
    x=getaddat(lis['id'])
    x['poster']=cast_image(lis['id'],lis['name'])
    x['name']=lis['name']
    if lis['gender']==1:
        x['gender']='Female'
    if lis['gender']==2:
        x['gender']='Male'
    if lis['gender']>2:
        x['gender']='Other'
    return x
def get_prod(a):
    url='https://api.themoviedb.org/3/search/company?api_key='+api_key+'&page=1&query='+a
    r=requests.get(url)
    r=r.json()
    lis = [(k, v) for k, v in r.items()]
    lis=lis[1][1][0]
    url='https://api.themoviedb.org/3/company/'+str(lis['id'])+'?api_key='+api_key
    r=requests.get(url)
    r=r.json()
    poster=requests.get(url=poster_url+r['logo_path'])
    poster=poster.content
    a=r['name']
    file = open("static/production/im_"+a+".png", "wb")
    file.write(poster)
    file.close() 
    r['poster']="/production/im_"+a+".png"
    return r
def get_director(a):
    url='https://api.themoviedb.org/3/search/person/?api_key='+api_key+'&language=en-US&page=1&include_adult=false&query='+a
    r=requests.get(url=url)
    r=r.json()
    lis = [(k, v) for k, v in r.items()]
    lis=lis[1][1][0]
    x=getaddat(lis['id'])
    x['poster']=lis['profile_path']
    poster=requests.get(url=poster_url+x['poster'])
    poster=poster.content
    a=lis['name']
    file = open("static/directors/im_"+a+".png", "wb")
    file.write(poster)
    file.close() 
    x['poster']="/directors/im_"+a+".png"
    if lis['gender']==1:
        x['gender']='Female'
    if lis['gender']==2:
        x['gender']='Male'
    if lis['gender']>2:
        x['gender']='Other'
    return x

def get_actornames(df):
    h=[]
    a=[]
    for i in df["actor1"]:
        i=" ".join(re.split('(?=[A-Z])', i))
        i=i.strip(" ")
        a.append(i)
    for i in df["actor2"]:
        i=" ".join(re.split('(?=[A-Z])', i))
        i=i.strip(" ")
        a.append(i)
    for i in df["actor3"]:
        i=" ".join(re.split('(?=[A-Z])', i))
        i=i.strip(" ")
        a.append(i)
    k=Counter(a)
    k=dict(k)
    for i,j in k.items():
       if j>4:
           h.append(i) 
    return h
def get_productionnames(df):
    pro=[]
    for i in df["production"]:
        i=" ".join(re.split('(?=[A-Z])', i))
        i=i.strip(" ")
        pro.append(i)
    k=Counter(pro)
    
    h2=[]
    k=dict(k)
    for i,j in k.items():
        if j>4:
            h2.append(i) 
    return h2
def get_directornames(df):
    dir1=[]
    for i in df["director"]:
        i=" ".join(re.split('(?=[A-Z])', i))
        i=i.strip(" ")
        dir1.append(i)
    k=Counter(dir1)
    h1=[]
    k=dict(k)
    for i,j in k.items():
        if j>4:
            h1.append(i) 
    return h1

if __name__ == "__main__":
    df=pd.read_csv('temp1.csv')
    actorname=get_actornames(df)
    directorname=get_directornames(df)
    productionname=get_productionnames(df)
    app.run(debug=True,port=8000) 

