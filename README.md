# What is Gibbs?
Gibbs essentially takes the url of an Anime-filled Open directory then searches the list of anime on Myanimelist.com using an unofficial api found @ (https://pypi.org/project/mal-api/). It's useful for when you have found an Open directory filled with anime and you want to know which ones are any good so that you can download them, opposed to manually copying and pasting each title in the OD yourself.

# How to use
  1. Import the Gibbs class
  2. Create Gibbs object: 
      - You have the option of adding a numpy array of stopwords. These are strings that you repeatedly see in the OD that might cause bad search results.
  3. Call getMalInfo(<OD url>) on your objects to get a table with the anime's titles, scores and descriptions as columns.
     - You can use getAnimeList() to get a list of the anime result objects and use them. (The mal-api will help you with that)
     - saveAnimeList('directory/filename.html') will save the latest anime table in an html file.
  
  *The speed of the program is limited by the speed of the mal-api.
  
# Dependencies

- urllib : for server queries
- bs4 (BeautifulSoup): for scraping
- mal :  myanimelist api
- plotly: for plotting the results' table
