from collections import Counter
import re
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