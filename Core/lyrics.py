def songlyrics(url):
    import requests
    import json
    import pafy

    try:
        video = pafy.new(url)
        artist = video.author
        if 'vevo' in artist:
            artist = artist.replace("vevo", "")
        elif 'Vevo' in artist:
            artist = artist.replace("Vevo", "")
        elif 'VEVO' in artist:
            artist = artist.replace("VEVO", "")

        if artist.lower() == "hybe labels":
            artist = "BTS"
        elif artist.lower() == "imaginedragons":
            artist = "Imagine Dragons"
        elif artist.lower() == "thescore":
            artist = "The Score"

        song = video.title
        song = song.lower()
        if artist.lower() in song:
            song = song.replace(artist.lower(), "")
        if 'ft' in song:
            song = song.replace('ft', "")
        if '-' in song:
            song = song.replace('-', "")
        if '.' in song:
            song = song.replace('.', "")
        if 'official' in song:
            song = song.replace('official', "")
        if 'music' in song:
            song = song.replace('music', "")
        if 'audio' in song:
            song = song.replace('audio', "")
        if 'video' in song:
            song = song.replace('video', "")
        if 'lyrics' in song:
            song = song.replace('lyrics', "")
        if '(' in song:
            song = song.replace('(', "")
        if ')' in song:
            song = song.replace(')', "")
        if '[' in song:
            song = song.replace('[', "")
        if ']' in song:
            song = song.replace(']', "")
        if '{' in song:
            song = song.replace('{', "")
        if '}' in song:
            song = song.replace('}', "")
        if 'screen' in song:
            song = song.replace('screen', "")
        songlst = song.split()
        for i in songlst:
            try:
                xyz = 'https://api.lyrics.ovh/v1/'+artist+'/'+i
                response = requests.get(xyz)
                json_data = json.loads(response.content)
                if "lyrics" in json_data.keys():
                    lyrics = json_data['lyrics']
                    break
                else:
                    lyrics = "Lyrics Unavailable"
            except:
                lyrics = "Lyrics Unavailable"
                continue
        return lyrics
    except:
        pass
