from typing import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from secret import spotipy_api_secrets

class SpotifyPlaylistMaker:
    def __init__(self) -> None:
        self.total_read_tracks = 0
        self.total_valid_tracks = 0
        self.remove_count = 0
        self.tracks = []
        self.removed_tracks = set()
        self.track_features = {}

        self.min_bpm = None
        self.max_bpm = None
        self.min_energy = None
        self.min_danceability = None

        scope = "playlist-modify-public"
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(spotipy_api_secrets['client_id'], spotipy_api_secrets['client_secret'], spotipy_api_secrets['redirect_uri'], scope=scope)
        )
        self.user_id = self.sp.me()['id']
    
    def get_playlist_tracks(self, playlist_url: str) -> Set[dict]:
        tracks = set()
        playlist_id = playlist_url.split("/")[-1].split("?")[0]
        result = self.sp.playlist_tracks(playlist_id, fields="items(track(name,id,is_local,available_markets)),next", limit=50)
        items = result['items']
        while result['next']:
            result = self.sp.next(result)
            items.extend(result['items'])
        self.total_read_tracks += len(items)

        for x in items:
            track = x['track']
            if track and 'US' in track['available_markets'] and not track['is_local']:
                tracks.add(track['id'])
        
        print("Found {} tracks in playlist {}.".format(len(tracks), playlist_id))
        return tracks
    
    def set_all_tracks(self, playlist_urls: List[str] ) -> List[dict]:
        tracks = set()
        for playlist_url in playlist_urls:
            tracks.update(self.get_playlist_tracks(playlist_url))
        self.tracks = list(tracks)
        self.total_valid_tracks = len(self.tracks)
    
    def get_all_track_features(self) -> None:
        if self.tracks == []:
            raise Exception("No tracks to get features for! Please call set_all_tracks([<playlist url strings>]) first.")
        self.track_features = {}
        for i in range(0,self.total_valid_tracks,100):
            subset = self.tracks[i:i+100]
            features = self.sp.audio_features(subset)
            id_features = zip(subset, features)
            for id, feature in id_features:
                if feature is None:
                    print(f'No features for {id}')
                    self.remove_count += 1
                    self.removed_tracks.add(id)
                    continue
                self.track_features[id] = feature
    
    def remove_tracks(self) -> None:
        self.tracks = [x for x in self.tracks if x not in self.removed_tracks]
        self.removed_tracks = set()
        self.get_all_track_features()
        
    def remove_bad_bpm_tracks(self, min_bpm: int, max_bpm=None) -> None:
        for id, feature in self.track_features.items():
            tempo = feature['tempo']
            if (min_bpm is not None and tempo < min_bpm) or (max_bpm is not None and tempo > max_bpm):
                self.removed_tracks.add(id)
                self.remove_count += 1
        
        print("From {} tracks, found {} valid tracks with BPM inside of {}-{} range.".format(len(self.tracks), len(self.tracks) - len(self.removed_tracks), min_bpm, max_bpm))
        self.remove_tracks()

    def remove_bad_energy_tracks(self, min_energy:float) -> None:
        for id, feature in self.track_features.items():
            energy = feature['energy']
            if energy < min_energy:
                self.removed_tracks.add(id)
                self.remove_count += 1
        
        print("From {} original tracks, found {} valid tracks with energy greater than {}.".format(len(self.tracks), len(self.tracks) - len(self.removed_tracks), min_energy))
        self.remove_tracks()
    
    def remove_bad_danceability_tracks(self, min_danceability:float) -> None:
        for id, feature in self.track_features.items():
            danceability = feature['danceability']
            if danceability < min_danceability:
                self.removed_tracks.add(id)
                self.remove_count += 1
        print("From {} original tracks, found {} valid tracks with danceability greater than {}.".format(len(self.tracks), len(self.tracks) - len(self.removed_tracks), min_danceability))
        self.remove_tracks()
    
    def remove_invalid_tracks(self) -> None:
        self.get_all_track_features()
        if self.min_bpm is not None or self.max_bpm is not None:
            self.remove_bad_bpm_tracks(self.min_bpm, self.max_bpm)
        if self.min_energy is not None:
            self.remove_bad_energy_tracks(self.min_energy)
        if self.min_danceability is not None:
            self.remove_bad_danceability_tracks(self.min_danceability)
    
    def reorder_tracks(self,type:str):
        self.get_all_track_features()
        if type == 'bpm':
            self.tracks.sort(key=lambda x: self.track_features[x]['tempo'])
        elif type == "bpm_bounce":
            self.tracks.sort(key=lambda x: self.track_features[x]['tempo'])
            self.tracks = self.tracks[::2]+self.tracks[::-1][len(self.tracks)%2::2]
        elif type == 'energy':
            self.tracks.sort(key=lambda x: self.track_features[x]['energy'])
        elif type == 'popularity':
            self.tracks.sort(key=lambda x: self.track_features[x]['popularity'], reverse=True)
        elif type == 'danceability':
            self.tracks.sort(key=lambda x: self.track_features[x]['danceability'])
        else:
            raise Exception("Invalid type for reorder_tracks. Valid types are 'bpm', 'bpm_bounce', 'energy', 'popularity', and 'danceability'.")
        
    
    def make_playlist(self, playlist_name=None, edit_playlist_url=None) -> str:
        if (playlist_name is None and edit_playlist_url is None) or (playlist_name is not None and edit_playlist_url is not None):
            raise Exception("Must provide either a playlist name or an edit playlist url.")
        if len(self.tracks) != self.total_valid_tracks - self.remove_count:
            raise Exception("Something went wrong: {} good tracks, {} removed tracks, {} total tracks".format(len(self.tracks), self.remove_count, self.total_valid_tracks))

        playlist_id = None
        if edit_playlist_url:
            playlist_id = edit_playlist_url.split("/")[-1].split("?")[0]
            self.sp.user_playlist_replace_tracks(user=self.user_id, playlist_id=playlist_id, tracks=[])  # clear playlist
        else:
            result = self.sp.user_playlist_create(user=self.user_id, name=playlist_name)
            playlist_id = result['id']

        for i in range(0,len(self.tracks),100):
            subset = self.tracks[i:i+100]
            self.sp.user_playlist_add_tracks(user=self.user_id, playlist_id=playlist_id, tracks=subset)

        print("{} playlist: {} with {} total songs".format("Edited" if edit_playlist_url else "Created", playlist_id if edit_playlist_url else playlist_name, len(self.tracks)))
        return playlist_id

    def set_min_energy(self, min_energy: float) -> None:
        self.min_energy = min_energy
    def set_min_bpm(self, min_bpm: int) -> None:
        self.min_bpm = min_bpm
    def set_max_bpm(self, max_bpm: int) -> None:
        self.max_bpm = max_bpm
    def set_min_danceability(self, min_danceability: float) -> None:
        self.min_danceability = min_danceability