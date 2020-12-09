#!/usr/bin/env python
# coding: utf-8

# ## This is my first attempt at scraping the html of a movie OD page. Then I will use the gathered movie names to check their respective idmb ratings

# In[1]:


import sys

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

from bs4 import BeautifulSoup
import wikipedia
from wikipedia.exceptions import PageError
from wikipedia.exceptions import DisambiguationError

from mal import *

import numpy as np
from tabulate import tabulate
    
    


# In[31]:


class Gibbs:
    def __init__(self, my_stopwords = np.empty(shape=0)):
        self.__animeList = np.empty(shape=0)
        
        #words or strings of symbols that we want removed to get the movie/series title
        self.__stopwords =  np.array(['/','10bit','BluRay','Dual Audio', 'AAC','1080p','720p','480p','x264','x265','.mkv', '.mp4','WEBRip', '[', ']','(',')'])
        self.__stopwords = np.append(my_stopwords,self.__stopwords)
    
    
    #________________________________ INTERFACE _______________________
    
    #FOR AN OPEN DIR WITH ANIME:
    def getMalInfo(self, dirUrl):
        titles = self.__getList(dirUrl)
        
        if titles == None:
            return
        
        #get the names and try to clean them
        for item in titles:
            name = item.get_text() #remove tags and other html code
            name = self.__cleanName(name)
        
            #search on my animelist and save the top result
            try: #if there is no error then store the anime object
                search = AnimeSearch(name)
                res = search.results[0]
                self.__animeList = np.append(self.__animeList,res)
            except:
                e = sys.exc_info()[0]
                print("[ " + name + " ] raised the following error:", end=' ')
                print(e)
        
        #print the successfully returned anime with scores, nr of episodes etc
        self.__getAnimeTable(self.__animeList)
    
    #RETURNS LIST OF ANIME RESULTS FROM MAL
    def getAnimeList(self):
        return self.__animeList
    
    #______________ WORKERS ______________
    
    #PRINTS A TABLE WITH ANIME DETAILS
    def __getAnimeTable(self, animeList):
        import plotly.graph_objects as go

        #Stores the entries for each column
        titles = []
        scores = []
        synops = []

        for anime in animeList:
            titles.append(anime.title)
            scores.append(anime.score)
            synops.append(anime.synopsis + '[' + anime.url + ']')

        #build the table to be shown
        fig = go.Figure(
            data=[go.Table(
                columnwidth=[100,26, 500],
                header=dict(
                    values=['Title', 'Score','Synopsis']),
                cells=dict(
                    values=[titles, scores, synops],
                    align='left',
                    height= 100)
                )]
        )
        fig.show()
    
    #takes in a string and then replaces any occurences of the stop words with an empty string
    def __cleanName(self, string):
        for sw in self.__stopwords:
            string = string.replace(sw, "")
        return string
    
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

