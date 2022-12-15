Readme
CS539 Machine Learning Project Website Fall 2022 (By Gabrielle Cabebe, Agustina Maccio, Tess Royds, Adityavikram Gurao, Uday Kumbhar)
You can check the website :
http://ady24kxy10.pythonanywhere.com/

This is our project website for Machine Learning CS539 (Fall 2022). In this project, 
we are proposing a tool to generate ‘friendships’ based on musical preferences and playlist composition of Spotify users. 
The tool will take a user’s Spotify playlist(s) as input and create matches with other Spotify users based on an algorithmic compatibility of the audio features of songs within each playlist.
Research suggests that music has the power to bring people together, and that is the motivation behind this proposal. 
Though this project will be small-scale, Spotify is one of the largest music streaming services in the world, with over 433 million users. 
The idea itself has the potential to allow people to make connections with others around the world who find pleasure in the same types of music. 
We have tested the tool before implementing into a website. When user input their name and playlist link, the tool will give a name of matched person, 
name of their playlist and playlist link they got matched to from our data. We are analyzing data using criteria that do not take into account the lingual aspect of the songs, 
there may be some linguistic bias, but we will be able to identify people who enjoy similar music based on attributes of the song rather than the language spoken.

Playlist links were collected from our classmates with their consent to use this data for ML Project purpose. 
Since data collected was not sufficient to give better results, we also collected public playlists from online available resources. 
While working on website locally, we found out when it tries to make a spiderplot for user and matched person, 
it'll take significant amount of time or fails to load if the playlist contains more than 100 songs due to limitations of spotify's API. 
Generally, on an average a playlist should contain in between 50-80 songs. 
But sometimes their could be more than 100 songs. 
In order to run the website locally, you need to download this folder. 
Before running the website locally you need to install some files which can be found in requirements.txt (Use "pip install -r requirements.txt"(without quotes) for installing all the required packages). 
After installing all the required files, run the setup.py file using " python setup.py "(without quotes).
