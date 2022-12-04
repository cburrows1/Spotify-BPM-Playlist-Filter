from SpotifyPlaylistMaker import SpotifyPlaylistMaker

playlist_urls = [
    "https://open.spotify.com/playlist/37i9dQZF1DXat5j4Lk8UEj?si=3973deef1bd04817", # Folk Rock Favorites - 100 songs
    "https://open.spotify.com/playlist/37i9dQZF1DWSgQ5Y8XEtFi?si=9124100c8b0e421b", # Lockjaw - 50 songs
    "https://open.spotify.com/playlist/16e0fS65JQsToxR3hxufzV?si=c6103605f14c46df", # songs I wish i could listen to for the first time again - 100 songs - 29 songs
    "https://open.spotify.com/playlist/3baQvj17epnxzewdyOIpIJ?si=95471e0ce9954cbb", # Energetic House - 105 songs
    "https://open.spotify.com/playlist/6TWgOtrMBa1JTdeS7ImnDd?si=965f53c6cf184298", # Gym Rap and Hardstyle - 224 songs
    "https://open.spotify.com/playlist/0Ur30xkD1qsIodE9LKqBOg?si=21e6c9e13150418a", # Kanye Bangers - 94 songs
    "https://open.spotify.com/playlist/4oOv0CVyh6yZTMUuzpuC2u?si=1ace2042313f4ab0", # GOMDB - 137 songs
    "https://open.spotify.com/playlist/5mnU2v77xvzSQCclBEtT6f?si=273ac0e808ed4b4f", # Big nuts in my mouth - 94 songs
    "https://open.spotify.com/playlist/2lk6445GUpENJLdDyJFMHJ?si=207ac3509f18459b", # 100 best ROCK WORKOUT SONGS - 101 songs
    "https://open.spotify.com/playlist/2vvlkzf1hO1IAtGAITdEVE?si=dcdf798e335d4ecd", # Pump Up Rock - 280 songs
    "https://open.spotify.com/playlist/4bvh3D3jZ4xhCixsl6BKjT?si=b44d785d67444a37", # SONGS THAT ARE 100% PERFECTION - 148 songs
    "https://open.spotify.com/playlist/7a5ef1Rd6EF1VqM8XMZN8I?si=a6b612e71d764603", # Biking playlist - 424 songs
    "https://open.spotify.com/playlist/0UBFYlt0AL04qINqhHYy36?si=4287744bed904fab", # Best running playlist ever - 79 songs
    "https://open.spotify.com/playlist/4PYYrTwEUdtpsjdfXdTIGX?si=4bf4394633ef4762", # Hip Hop/Rap songs that everyone knows except you - 142 songs
    "https://open.spotify.com/playlist/78T2QXH8fAyIfByeD4CANw?si=ca96282b6b224bde", # songs that are perfect - 97 songs
    "https://open.spotify.com/playlist/37i9dQZF1DX97h7ftpNSYT?si=9f85e9b32de14096", # I love my 2010s Hip-Hop - 100 songs
    "https://open.spotify.com/playlist/37i9dQZF1DWUX4dHd4gmc7?si=a5b7f5538f644bc5", # Workout Hip-Hop - 82 songs
    "https://open.spotify.com/playlist/37i9dQZF1DWT5MrZnPU1zD?si=edb3c2ef787d47e4", # Hip Hop Controller - 100 songs
    "https://open.spotify.com/playlist/37i9dQZF1DWTyiBJ6yEqeu?si=bf3e1993c0514d0e", # Top Gaming Tracks - 100 songs
    "https://open.spotify.com/playlist/37i9dQZF1DWWPcvnOpPG3x?si=c0836d3238004c85", # Run this town - 50 songs
    "https://open.spotify.com/playlist/37i9dQZF1DX3oM43CtKnRV?si=3776ada4c7ed4af7", # 00s Rock Anthems - 100 songs
    "https://open.spotify.com/playlist/2pVWj9B06NrUNjLCQC9XJP?si=e59aac6671184851", # workout songs that make me feel like cbum - 66 songs
    "https://open.spotify.com/playlist/0JtK8ZG5Ir5j9EBraH0nA2?si=076bcddc9af64674", # Trap Metal, Phonk, Hardstyle, Rock, Training, Rap - 571 songs
]

EDIT_PLAYLIST = True # if True, edit playlist in place. Else, create new playlist based on playlist_urls

edit_playlist_url = "https://open.spotify.com/playlist/69x4kswf9xRWYf7ySFcml5?si=e1e91d78c5e8402b"
playlist_name = "165 BPM All Workout Playlist"

min_bpm = 165
max_bpm = None
min_energy = 0.65
min_danceability = 0.65
track_sort = "bpm_bounce"

## Edit above this line ##

playlist_maker = SpotifyPlaylistMaker()
playlist_maker.set_min_bpm(min_bpm)
playlist_maker.set_max_bpm(max_bpm)
playlist_maker.set_min_energy(min_energy)
playlist_maker.set_min_danceability(min_danceability)

playlist_maker.set_all_tracks([edit_playlist_url] if EDIT_PLAYLIST else playlist_urls)
playlist_maker.remove_invalid_tracks()
playlist_maker.reorder_tracks(track_sort)

if EDIT_PLAYLIST:
    playlist_maker.make_playlist(playlist_name=playlist_name)
else:
    playlist_maker.make_playlist(edit_playlist_url=edit_playlist_url)