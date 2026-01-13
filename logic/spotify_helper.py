import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyHelper:
    """
    Wrapper for the Spotipy library to handle Spotify API interactions.
    
    This class manages authentication using Client Credentials flow and 
    provides simplified methods for searching tracks.
    """
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.sp = None
        self.authenticate()

    def authenticate(self):
        if self.client_id and self.client_secret:
            try:
                auth_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
                self.sp = spotipy.Spotify(auth_manager=auth_manager)
                return True
            except Exception as e:
                print(f"Auth failed: {e}")
                return False
        return False

    def search_track(self, query, limit=10):
        if not self.sp:
            if not self.authenticate():
                raise Exception("Spotify authentication missing or failed.")
        
        try:
            results = self.sp.search(q=query, limit=limit, type='track')
            return results['tracks']['items']
        except Exception as e:
            raise Exception(f"Search failed: {e}")
