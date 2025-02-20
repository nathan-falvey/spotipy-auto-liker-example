import spotipy
import time
from spotipy.oauth2 import SpotifyOAuth


SPP_USERNAME = ""
SPP_KEY = ""
SPP_REDIRECT_URI = ""
MINIMUM_PERCENT = 89
scope = 'user-read-playback-state,user-library-read,user-library-modify'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPP_USERNAME,client_secret=SPP_KEY,redirect_uri=SPP_REDIRECT_URI,scope=scope,open_browser=True))


def like_song(id):
    results = sp.current_user_saved_tracks_contains(tracks=[id])
    if results == [False]:
        sp.current_user_saved_tracks_add(tracks=[id])
        return True
    else:
        return False

def has_active_device():
    devices = sp.devices()
    for device in devices['devices']:
        if device['is_active']:
            return True
    return False

while True:
    if has_active_device():
        current = sp.current_playback(market=None, additional_types=None)
        if current['currently_playing_type'] == 'track' and current['is_playing'] == True:
            required_ms = current['item']['duration_ms'] * (MINIMUM_PERCENT / 100)
            if current['progress_ms'] > required_ms:
                id = current['item']['id']
                like_song(id)
        time.sleep(3)
    else:
        time.sleep(5)