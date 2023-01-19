import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth

#initialize and authenticate spotify object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='goes here',
                                               client_secret='goes here',
                                               redirect_uri='Enter Redirect URI here',
                                               scope=['user-library-read','user-library-modify','playlist-modify-public','playlist-modify-private']))

#returns data frame of the top tracks of a user
def get_top_tracks(username,time_range):
    # Get the top tracks of a user
    topTracks = sp.current_user_top_tracks(time_range=time_range,limit=100)
    trackData = []
    for track in topTracks['items']:
        trackData.append([track['name'],track['artists'][0]['name'],track['popularity'],track['album']['name'],track['id']])
    trackDf = pd.DataFrame(trackData,columns=['Track Name','Artist','Popularity','Album','Track ID'])
    return trackDf

#creates a playlist with the given name and adds the tracks in the given data frame
def create_playlist(playlist_name,tracks_df):
    # Create a new playlist
    playlist = sp.user_playlist_create(user=username, name=playlist_name)
    playlist_id = playlist['id']
    track_ids = tracks_df['Track ID'].tolist()
    sp.playlist_add_items(playlist_id=playlist_id, tracks=track_ids)
    return playlist_id

#   returns a data frame of recommended songs based on the given seed tracks and target attributes
def recommend_songs(seed_tracks,target_attributes):
    # Get recommendations based on seed tracks
    recommendations = sp.recommendations(seed_tracks=seed_tracks, target_attributes=target_attributes)
    rec_tracks = recommendations['tracks']
    rec_tracks_data = []
    for track in rec_tracks:
        rec_tracks_data.append([track['name'],track['artists'][0]['name'],track['popularity'],track['album']['name'],track['id']])
    rec_tracks_df = pd.DataFrame(rec_tracks_data,columns=['Track Name','Artist','Popularity','Album','Track ID'])
    return rec_tracks_df

#Test case
username = 'avaneeshs'
top_tracks_df = get_top_tracks(username,'short_term') 
playlist_id = create_playlist("My Top Tracks (Short Term)",top_tracks_df) 
seed_tracks = top_tracks_df['Track ID'].tolist() 
target_attributes = ['danceability','energy'] #['danceability','energy','valence','acousticness','instrumentalness','liveness','speechiness','tempo
rec_tracks_df = recommend_songs(seed_tracks,target_attributes) 
create_playlist("Recommended Tracks based on my top tracks (Medium Term)",rec_tracks_df)
