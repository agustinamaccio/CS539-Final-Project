# CS539-Final-Project

## Project Scope
 
In this project, we are proposing a tool to generate ‘friendships’ based on musical preferences and playlist composition of Spotify users. The tool will take a user’s Spotify playlist(s) as input and create matches with other Spotify users based on an algorithmic compatibility of the audio features of songs within each playlist.

In this repository you will find the following directories:
1. SpotifyDataScraping: includes a python script which reads a csv file with spotify playlist links, and scrapes the data using the Spotify API ans spotypy library. It also includes the csv with the links. 

2. Models: includes 4 different python files for the 4 different models that we developed for clustering the data. Each file includes preprocessing steps. 
  2.1 K-means script
  2.2 DBSCAN
  2.3 OPTICS
  2.4 Agglomerative Hierarchical Clustering
