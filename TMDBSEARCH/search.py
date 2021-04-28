
api_key='ef83cac599a8b6b59be433cffe4aa715'
url='https://api.themoviedb.org/3/search/movie?api_key=' +api_key+ '&query='
poster_url='https://image.tmdb.org/t/p/original'
import pandas as pd
import numpy as np
import json
import requests
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
    n=n.replace(' ','_')
    n =n.replace('à', 'a')
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
    a=a.replace(' ','_')
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
    a=a.replace(' ','_')
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
if __name__ == '__main__':
    get_director("Christopher Nolan")