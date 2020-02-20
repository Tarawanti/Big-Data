#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 17:30:03 2020

@author: tarawantikhatri
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statistics as st
 

pd.options.display.max_rows = 20
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('datasets/movielens/users.dat', sep='::',
                      header=None, names=unames)

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('datasets/movielens/ratings.dat', sep='::',
                        header=None, names=rnames)

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('datasets/movielens/movies.dat', sep='::',
                       header=None, names=mnames)
#1----------------------------------------------------
data=pd.merge(users, ratings, on='user_id', how='outer')
df=pd.merge(data, movies, on='movie_id', how='outer')
df2=df.isnull().any(axis=1).to_frame()# row with missing values
print("\n\n1: Total number of rows with missing values=", df2[df2[0] == True].count())
df= df.dropna()

#2----------------------------------------------------
movie=df['movie_id'].nunique() 
genres=df['genres'].nunique()
users=df['user_id'].nunique()  
ratings=df['rating'].count()
typeratings=df.groupby('rating')['rating'].count()

print("\n\n2.1: Total number of movies:",movie)
print("2.2: Total number of genres:", genres)
print("2.3: Total number of users:", users)
print("2.4: Total number of ratings:", ratings, typeratings)
 
 
#3----------------------------------------------------
 
#3.1
 
 
print("\n\n3.1: Number of ratings per user")
ratingPerUser=df.groupby('user_id')['rating'].count()
#print(ratingPerUser)
plt.title("Number of ratings per user")
plt.bar(x=df.groupby('user_id')['rating'].count().index, align='center', alpha=1, color='black' ,linestyle='dashed', height=df.groupby('user_id')['rating'].count().values, width=3)
plt.show()
 
 

#3.2

def get_digit(s):
    """ extracting digits in a string and joining them into a string"""
    
    return ''.join([ i for i in s if i.isdigit()])
def get_year():
    str_list=df['title']
    
    s = [ i.replace('(','').replace(')','') for i in str_list]
    s2 = [i.split() for i in s]

#check the last string i[-1] in each list of strings, 
#if it is not a digit sequence then trying to extract digits    
    y_list = [i[-1] if i[-1].isdigit() and len(i[-1])==4 else get_digit(i[-1]) for i in s2]
    
    return pd.Series([ int(i) if len(i) > 0 else np.nan for i in y_list])

year=get_year()
df['Year'] = year
print("3.2: Number of Movie Per Year")
plt.title("Number of Movie Per Year")
plt.bar(x=df.groupby('Year')['movie_id'].count().index,
        align='center', alpha=1, color='black' ,linestyle='dashed',
        height=df.groupby('Year')['movie_id'].count().values, width=2)
plt.show()


#3.3
print("3.3: Number of Movie Per Genres")
plt.title("Number of movie Per Genres")
plt.bar(x=df.groupby('genres')['movie_id'].count().index, align='center', alpha=1, color='black' ,linestyle='dashed' , height=df.groupby('genres')['movie_id'].count().values, width=3) 
plt.show()  

#3.4 
print("Average ratings per movie")
plt.title("Average ratings per movie")
plt.bar(x=df.groupby('title')['rating'].mean().index, color='black', alpha=1, align='center',height=df.groupby('title')['rating'].mean().values, width=1) 
plt.show()

#3.5
print("3.5 Average ratings per genre")
plt.title("Average ratings per genre")
plt.bar(x=df.groupby('genres')['rating'].mean().index, color='black', height=df.groupby('genres')['rating'].mean().values, width=1)
plt.show()
   
#4----------------------------------------------------
#4.1
print("\n\n4.")
print("\n4.1")
 
#4.2
medianRating = df.groupby('user_id')['rating'].count().median()
print(medianRating)
Median = df.groupby('user_id')['rating'].count().\
            apply(lambda x: x>medianRating).to_frame()
Median = Median[Median['rating'] == True]
print("Number of users whose number of ratings are greater or equal to the",
      "median of the number of ratings are", len(Median))

print("4.2.")
print("Top ten movies with title and genres rated by each user from (1)\n") 
print(df[df.user_id.isin(Median.index)].groupby(['movie_id'])['rating'].mean().to_frame().sort_values('rating', ascending=False).head(10))

print("4.3")
print("Average rating per genre for each user from (1)\n",
      df[df.user_id.isin(Median.index)].\
      groupby(['user_id', 'genres'])['rating'].mean())