# Welcome to TuneTagger!

This is an interactive, full-stack web app built using **Python**, **Flask**, and **Vanilla HTML/CSS/JavaScript**. The purpose of this project is to provide music listeners with a more dynamic listening experience, being able to sort their playlists by mood, not  just genre or duration.


# Running

To run the project, simply visit this website:
https://tunetagger.onrender.com
It may take a moment to load, but not everyone is a millionaire...

# Workflow

TuneTagger would not be able to function without the Genius API! This API allows the user to fetch song lyrics, as well as annotation for each lyric. The backend of this project is built using a SQLite database for storage on the disk, as well as the VADER semantic analyzer for NLP of the lyrical and annotational details to determine a mood. 

- The user first enters a song and artist name
- These two fields will be stored in the SQLite database, and these two fields will be used to query the Genius API for their lyrical and annotational content. Once this information is recieved, the content is fed into the NLP model to determine the mood of the song
- Once the mood is fetched, this is also stored in the database, and rendered on the UI
- The user is then able to insert another song, remove songs, or filter their songs by mood
- Rinse repeat!



<img width="269" height="195" alt="tunetagger2 drawio" src="https://github.com/user-attachments/assets/11f35b0a-f415-4269-a02f-b4b0f30bf1d4" />

  
