"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re

# Custom Libraries
from utils.data_loader import load_movie_titles
from utils.data_loader import load_movie_budget
from utils.data_loader import load_movie_runtime
from utils.data_loader import load_movie_ratings
from utils.data_loader import load_movie_df
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Data Loading
movies = load_movie_df('resources/data/movies.csv')
movies = movies.dropna() 
title_list = load_movie_titles('resources/data/movies.csv')
imdb_data_budget = load_movie_budget('resources/data/imdb_data.csv')
imdb_data_runtime = load_movie_runtime('resources/data/imdb_data.csv')
ratings = load_movie_ratings('resources/data/ratings.csv')

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview","Exploratory Data Analysis (EDA)", "About Us"]   

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[0:819])
        movie_2 = st.selectbox('Second Option',title_list[820:1639])
        movie_3 = st.selectbox('Third Option',title_list[1639:2457])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")
               

    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.write("Describe your winning approach on this page")
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------
    if page_selection == "About Us":
        st.write('# Half Moon')
        st.write("# Movie Recommendations")
        #st.markdown("![Alt Text](https://media.giphy.com/media/xUNd9OwkwTb2GhJ7eo/giphy.gif)")
        st.write('In today’s technology driven world, recommender systems \
            are socially and economically critical to ensure that individuals can make optimised choices \
                surrounding the content they engage with on a daily basis. One application where this is especially \
                    true is movie recommendations; where intelligent algorithms can help viewers find great titles from tens of thousands of options.')
        
        st.write("##### Our Mission:")
        st.write("")
        st.write("##### our Vision")


    #---------------------------------------------------------------------------------------------------------------------------------------------------------
    if page_selection == "Exploratory Data Analysis (EDA)":
        
        st.markdown("<h1 style = 'text-align: center;'>Release Year Distribution</h1>", unsafe_allow_html=True)

        import plotly.figure_factory as ff
        #creating a new column for year
        
        movies['year'] = [x[-1].strip('()') for x in movies.title.str.split(" ")]
        
        num_pattern = r'^$|[a-zA-Z]|Τσιτσάνης|101次求婚|2006–2007|выбывание|پدر|Начальник|Джа|Девочки|первого'
        movies["year"] = movies["year"].replace(to_replace = num_pattern, value = np.nan, regex = True)
        year = [int(x) for x in movies["year"].dropna()]
        
        fig = plt.figure(figsize=(10,4))
        sns.histplot(year, kde = True,color = '#FF824E')
        plt.xlabel('Year')
        plt.xlim(left=1900, right = 2022)
        plt.title('Movie Release Year Distribution', fontweight = 'bold')
        st.pyplot(fig)
        st.write(f'Our model was trained on few 90s movie classics and a significant number 21st century movies')
        

        #Budget distribution plot
        st.markdown("<h1 style = 'text-align: center;'>Movie Budget Distribution</h1>", unsafe_allow_html=True)
        import string
        punctuations = string.punctuation 
        budget = []
        for text in imdb_data_budget.to_list():
            budget.append(int(re.sub('^[a-zA-Z]+','',text.translate(str.maketrans(' ',' ', punctuations)))))
        budget_df  = pd.DataFrame(budget, columns = ['budget'])
        fig = plt.figure(figsize=(10,4))
        sns.histplot(budget_df['budget'], bins=10000, color = '#FF824E')
        plt.xlabel('Budget')
        plt.xlim(left=0,right = 250000000)
        plt.title('Movie Budget Distribution', fontweight = 'bold')
        st.pyplot(fig)
        st.write(f'Average rating  database: {round(np.mean(budget_df["budget"]),2)} with a skewness to the right.')

        #movie ratings distribution Plot
        st.title('Movie Ratings Distribution')
        fig = plt.figure(figsize=(10,4))
        sns.boxplot(x = "rating", data=ratings, color = '#FF824E')
        plt.title('Movie ratings distribution', fontweight = 'bold')
        plt.show()
        st.pyplot(fig)
        st.write(f'Average rating  database: {round(np.mean(ratings["rating"]),2)} with 75% of the rating greater than 3.')
        
        #movie runtime Distribution 
        st.markdown("<h1 style = 'text-align: center;'>Movie Runtime Distribution</h1>", unsafe_allow_html=True)
        fig = plt.figure(figsize=(10,4))
        sns.histplot(imdb_data_runtime, kde = True, color = '#FF824E')
        plt.xlabel('Runtime (min)')
        plt.xlim(left = 0,right = 250)
        plt.title('Movie Runtime Distribution', fontweight = 'bold' )
        st.pyplot(fig)
        st.write(f'Average rating  database: {round(np.mean(imdb_data_runtime),2)} with a symetrical distribution')
    #---------------------------------------------------------------------------------------------------------------------------------------------


    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.

if __name__ == '__main__':
    main()
