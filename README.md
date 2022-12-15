# CS539-Final-Project-Spotability

## Website

You can check the website :
http://ady24kxy10.pythonanywhere.com/

## Project Scope
 
In this project, we are proposing a tool to generate ‘friendships’ based on musical preferences and playlist composition of Spotify users. The tool will take a user’s Spotify playlist(s) as input and create matches with other Spotify users based on an algorithmic compatibility of the audio features of songs within each playlist.

## Usage

In this repository you will find the following directories:
1. SpotifyDataScraping: includes a python script which reads a csv file with spotify playlist links, and scrapes the data using the Spotify API ans spotypy library. It also includes the csv with the links. 
  1.1 Get_track_info_per_playlist.ipynb
  1.2 PlaylistCollection.csv

2. FeatureEngineering: includes a python script for feature engineering and extraction as well as its inpus. Its inputs are the csv files generated from Get_track_info_per_playlist.py script.
  2.1 ConsolidateVariance.ipynb
  2.2 AllPlayslistData folder with csv files (inputs)

3. Models: includes 4 different python files for the 4 different models that we developed for clustering the data. Each file includes preprocessing steps. 
  3.1 K-means script
  3.2 DBSCAN
  3.3 OPTICS
  3.4 Agglomerative Hierarchical Clustering

4. Pipeline: includes a python script, a csv file and a pickle model. The Script file is a machine learning pipeline which automate the end-to-end workflow of our choseen clustering model (k-means). It takes a new playlist link and user name and returns its match. The csv file has information about the clusters created with the k-means model, and the pickle file contains the model it self.
  4.1 model.pkl
  4.2 pipeline_data
  4.3 script.ipynb
