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