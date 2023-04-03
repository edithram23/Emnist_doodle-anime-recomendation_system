import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
class pred:
    def recommend(self,name):
        df=pd.read_csv("anime.csv")
        
        for i in ["name","genre","type"]:
            df[i]=df[i].str.lower()
        
        df.dropna(inplace=True)
        Tf=TfidfVectorizer(stop_words='english')
        genre_dict = pd.DataFrame(data=df[['name','genre']])
        genre_dict.dropna(inplace=True)
        genre_dict.drop_duplicates(inplace=True)
        mat=Tf.fit_transform(genre_dict['genre'])
        similarity_matrix=linear_kernel(mat,mat)
        ind=pd.Series(genre_dict.index,index=genre_dict['name'])
        ind=ind.drop_duplicates()
        anime_index=ind[name]
        similarity_score = list(enumerate(similarity_matrix[anime_index]))
        similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        similarity_score = similarity_score[1:15]
        anime_indices = [i[0] for i in similarity_score]
        return list(genre_dict['name'].iloc[anime_indices])





