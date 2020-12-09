# What is Gibbs?
Pirate the Carribean(Open directories) more easily. Gibbs essentially takes the passed url of an Anime-filled Open directory then searches the list of anime on Myanimelist.com using their api (https://pypi.org/project/mal-api/). 

# How to use
  1. Import the Gibbs class
  2. Create Gibbs object: 
      - You have the option of adding a numpy array of stopwords. These are strings that you repeatedly see in the OD that might cause bad search results.
  3. Call getMalInfo(<OD url>) on your objects to get a table with the anime's titles, scores and descriptions as columns.
     - You can use getAnimeList() to get a list of the anime result objects and use them. (The mal-api will help you with that)
