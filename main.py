import spotipy
from spotipy.oauth2 import SpotifyOAuth

playlist_urls = [
    #"https://open.spotify.com/playlist/6TWgOtrMBa1JTdeS7ImnDd?si=1c13089ecced422d", # Gym Rap & Hardstyle - 213 songs
    #"https://open.spotify.com/playlist/3vVP7mntRIdq0i5bzvouMt?si=547648c120fc4c71", # Running Playlist 180 bpm - 44 songs
    #"https://open.spotify.com/playlist/4caZ0gjmOsYztmudFqdRXb?si=e391dd1d17924445", # DRILL SHIT KILL SHIT - 465 songs
    "https://open.spotify.com/playlist/37i9dQZF1DXat5j4Lk8UEj?si=3973deef1bd04817", # Folk Rock Favorites - 100 songs
    "https://open.spotify.com/playlist/0U5JlVYafbQ35qjWhQKUfp?si=4d4496e0acf24275", # Modern Folk Rock - 51 songs
    "https://open.spotify.com/playlist/2dUO8L5PCyBnN6tu6i9b6V?si=7c82128fb4b843a0", # Indie/Folk Rock - 508 songs
]
target_bpm = 180
tolerance = 0.05



scope = "playlist-modify-public"
client_id = "53ac7745b5f84f9397f7c15c13bae419"
client_secret = "c46f1d283fc94a27966c2d8450647030"
redirect_uri = "http://localhost:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope))

tracks = set()
for playlist_url in playlist_urls:
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    result = sp.playlist_tracks(playlist_id, fields="items(track(name,id,is_local,available_markets)),next", limit=50)
    items = result['items']
    while result['next']:
        result = sp.next(result)
        items.extend(result['items'])

    items_clean = [x['track']['id'] for x in items if not x['track']['is_local'] and 'US' in x['track']['available_markets']]
    tracks.update(items_clean)
tracks = list(tracks)

low_bpm = target_bpm * (1 - tolerance)
high_bpm = target_bpm * (1 + tolerance)

original_count = len(tracks)
bad_count = 0
for i in range(0,len(tracks),100):
    subset = tracks[i:i+100]
    features = sp.audio_features(subset)
    id_features = zip(subset, features)
    for id, feature in id_features:
        if feature is None:
            print(f'No features for {id}')
            continue
        tempo = feature['tempo']
        if tempo < low_bpm or tempo > high_bpm:
            tracks.remove(id)
            bad_count += 1

print("Found {} tracks with BPM inside of {}-{} range".format(original_count - bad_count, low_bpm, high_bpm))

user_id = sp.me()['id']

playlist_name = f"{target_bpm} BPM Generated Playlist"
result = sp.user_playlist_create(user=user_id, name=playlist_name)
playlist_id = result['id']

print("Created playlist: {}".format(playlist_name))

for i in range(0,len(tracks),100):
    subset = tracks[i:i+100]    
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=subset)