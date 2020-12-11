#!/usr/bin/env python
# coding: utf-8

# ## This is my first attempt at scraping the html of an OD page. Then I will use the gathered list of anime to search them on myanimelist.com

# In[94]:


import sys

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

from bs4 import BeautifulSoup

from mal import *

import numpy as np
    
    


# In[95]:


class Gibbs:
    def __init__(self, my_stopwords = np.empty(shape=0)):
        self.__animeList = np.empty(shape=0)
        self.__animeTable = None
        self.__animeUrl = None #most recent url for anime OD
        
        self.__movieList = np.empty(shape=0)
        self.__movieTable = None
        self.__movieUrl = None
        
        self.__seriesList = np.empty(shape=0)
        self.__seriesTable = None
        self.__seriesUrl = None
    
    
    #________________________________ INTERFACE _______________________
    
    #FOR AN OPEN DIR WITH live action Movies:
    def getMovieInfo(self,dirUrl,API_KEY="f877d4d3d3eec1a4054f59bbf9933930"):
        self.__movieUrl = dirUrl
        
        #scrape the movie titles
        titles = self.__getList(dirUrl)
        
        if titles == None:
            return
        
        #set up TMDb 
        from tmdbv3api import TMDb
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        
        #get the movie class
        from tmdbv3api import Movie
        movieApi = Movie()
       
        #do the search of the titles in TMDb
        for item in titles:
            name = item.get_text() #remove tags and other html code
                        
            #clean name using guessit
            name = self.__cleanName(name)
            
            try:
                #search given name and store the top result
                search = movieApi.search(name)
                
                if len(search) > 0:
                    top_result = search[0]
                    self.__movieList = np.append(self.__movieList,top_result)
                else:
                    print("< No result was found for ["+ name + "] >")
           
            except AttributeError as e:
                print("[ " + name + " ] raised the following AttributeError:", end=' ')
                print(e)
            except:
                e = sys.exc_info()[0]
                print("[ " + name + " ] raised the following error:", end=' ')
                print(e)
        
        #create and show a table for the results
        self.__showMSTable(self.__movieList,True)
        
    #FOR AN OPEN DIR WITH live action Series:
    def getSeriesInfo(self,dirUrl,API_KEY="f877d4d3d3eec1a4054f59bbf9933930"):
        self.__seriesUrl = dirUrl
        
        #scrape the movie titles
        titles = self.__getList(dirUrl)
        
        if titles == None:
            return
        
        #set up TMDb 
        from tmdbv3api import TMDb
        tmdb = TMDb()
        tmdb.api_key = API_KEY
        
        #get the movie class
        from tmdbv3api import TV
        tvApi = TV()
       
        #do the search of the titles in TMDb
        for item in titles:
            name = item.get_text() #remove tags and other html code
                        
            #clean name using guessit
            name = self.__cleanName(name)
            
            try:
                #search given name and store the top result
                search = tvApi.search(name)
                
                if len(search) > 0:
                    top_result = search[0]
                    self.__seriesList = np.append(self.__seriesList,top_result)
                else:
                    print("< No result was found for ["+ name + "] >")
           
            except AttributeError as e:
                print("[ " + name + " ] raised the following AttributeError:", end=' ')
                print(e)
            except:
                e = sys.exc_info()[0]
                print("[ " + name + " ] raised the following error:", end=' ')
                print(e)
        
        #create and show a table for the results
        self.__showMSTable(self.__seriesList, False)
        
    
    #FOR AN OPEN DIR WITH ANIME:
    def getMalInfo(self, dirUrl):
        self.__animeUrl = dirUrl
        titles = self.__getList(dirUrl)
        
        if titles == None:
            return
        
        config.TIMEOUT = 1  # set time out to 1 second
        #get the names and try to clean them
        for item in titles:
            name = item.get_text() #remove tags and other html code
            name = self.__cleanName(name)
        
            #search on my animelist and save the top result
            try: #if there is no error then store the anime object
                search = AnimeSearch(name)
                res = search.results[0]
                
                try:
                    full_anime = Anime(res.mal_id)
                    self.__animeList = np.append(self.__animeList,full_anime)
                except:
                    self.__animeList = np.append(self.__animeList,res)
            except AttributeError as e:
                print("[ " + name + " ] raised the following AttributeError:", end=' ')
                print(e)
            except:
                e = sys.exc_info()[0]
                print("[ " + name + " ] raised the following error:", end=' ')
                print(e)
        
        #print the successfully returned anime with scores, nr of episodes etc
        self.__showAnimeTable(self.__animeList)
        
    #RETURNS LIST OF ANIME RESULTS FROM MAL as np array
    def getMovieList(self):
        return self.__movieList
    
    #RETURNS LIST OF ANIME RESULTS FROM MAL as np array
    def getSeriesList(self):
        return self.__seriesList
    
    #RETURNS LIST OF ANIME RESULTS FROM MAL as np array
    def getAnimeList(self):
        return self.__animeList
    
    #STORES THE Movie TABLE INTO AN HTML FILE
    def saveMovieTable(self, name):
        import plotly
        #use plotly to save file
        plotly.offline.plot(self.__movieTable, filename=name)
        
    #STORES THE Movie TABLE INTO AN HTML FILE
    def saveSeriesTable(self, name):
        import plotly
        #use plotly to save file
        plotly.offline.plot(self.__seriesTable, filename=name)    
    
    #STORES THE ANIME TABLE INTO AN HTML FILE
    def saveAnimeTable(self, name):
        import plotly
        #use plotly to save file
        plotly.offline.plot(self.__animeTable, filename=name)
        
    
    #______________ WORKERS ______________

    #PRINTS A TABLE WITH MOVIE/Series DETAILS
    def __showMSTable(self, movieList, isMovie):
        import plotly.graph_objects as go

        #Stores the entries for each column
        indeces = []
        titles = []
        ratings = []
        overviews = []

        index = 0
        for movie in movieList:
            indeces.append(index)
            
            if isMovie: #since this will accomodate both series and movies 
                titles.append(movie.title)
            else:
                titles.append(movie.name)
            
            ratings.append(movie.vote_average)
            overviews.append(movie.overview)
            index = index + 1
            
        #build the table to be shown
        fig = go.Figure(
            data=[go.Table(
                columnwidth=[26,100,28, 500],
                header=dict(
                    values=['Index','Title', 'Rating','Overview']),
                cells=dict(
                    values=[indeces, titles, ratings, overviews],
                    align='left',
                    height= 100)
                )]
        )
        #set title of table
        if isMovie:
            table_title = "Movies in " + self.__movieUrl
            fig.update_layout(title_text= table_title)
            self.__movieTable = fig
        else:
            table_title = "Series in " + self.__seriesUrl
            fig.update_layout(title_text= table_title)
            self.__seriesTable = fig
        
        fig.show()
    
    
    
    #PRINTS A TABLE WITH ANIME DETAILS
    def __showAnimeTable(self, animeList):
        import plotly.graph_objects as go

        #Stores the entries for each column
        indeces = []
        titles = []
        scores = []
        synops = []

        index = 0
        for anime in animeList:
            indeces.append(index)
            titles.append(anime.title)
            scores.append(anime.score)
            synops.append('[' + anime.type + '] ' + anime.synopsis)
            index = index + 1
            
        #build the table to be shown
        fig = go.Figure(
            data=[go.Table(
                columnwidth=[26,100,26, 500],
                header=dict(
                    values=['Index','Title', 'Score','Synopsis']),
                cells=dict(
                    values=[indeces, titles, scores, synops],
                    align='left',
                    height= 100)
                )]
        )
        #set title of table
        table_title = "Anime in " + self.__animeUrl
        fig.update_layout(title_text= table_title)
        
        self.__animeTable = fig
        fig.show()
    
    #takes in a string and applies guessit to extract the title
    def __cleanName(self, string):
        from guessit import guessit
        
        guess = guessit(string)
        #if guessit guessed a title then return that
        try:
            name = guess['title']
        except:
            name = string
        
        return name
    
    #gets list of links(therefore movies/series from the given url)
    def __getList(self, url):
        try:
            html = urlopen(url)
        except HTTPError as e:
            print(e)
        except URLError as e:
            print('could not connect to server')
        else: 
            try:
                bs = BeautifulSoup(html, 'html.parser')
                titles = bs.find_all('a')
            except AttributeError as e:
                return None
            return titles

