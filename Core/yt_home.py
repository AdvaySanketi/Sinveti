def youtube_home():
    from youtubesearchpython import VideosSearch
    import urllib.request
    import random
    
    topiclist = ["official audio", "official video", "music", "english songs", "songs", "vevo", "Lyric video", "audio"]
    txt = random.choice(topiclist)
    videosSearch = VideosSearch(txt, limit = 6)
    name_lst = []
    url_lst = []
    for i in range(6):
        name_lst.append(videosSearch.result()['result'][i]['title'])
        url_lst.append(videosSearch.result()['result'][i]['link'])
        thumb_url = videosSearch.result()['result'][i]['thumbnails'][0]['url']
        file = "Thumbnails/"+str(i)+".jpg"
        urllib.request.urlretrieve(thumb_url, file)
    return name_lst, url_lst

def yt_search(search):
    from youtubesearchpython import VideosSearch
    import urllib.request

    txt = search + ' songs'
    videosSearch = VideosSearch(txt, limit = 8)
    name_lst = []
    url_lst = []
    for i in range(8):
        thumb_url = videosSearch.result()['result'][i]['thumbnails'][0]['url']
        name_lst.append(videosSearch.result()['result'][i]['title'])
        url_lst.append(videosSearch.result()['result'][i]['link'])
        file = "search_Thumbnails/"+str(i)+".jpg"
        urllib.request.urlretrieve(thumb_url, file)
    return name_lst, url_lst

def viddata(url):
    import youtube_dl
    import pafy
    import urllib.request
    from youtubesearchpython import VideosSearch
    import os

    try:
        video = pafy.new(url)
        videosSearch = VideosSearch(url, limit = 1)
        best = video.getbest(preftype = "mp4")
        path = os.getcwd() + "\\videos\\"
        best.download(filepath= path + video.videoid + ".mp4", quiet = True)
        thumb_url = videosSearch.result()['result'][0]['thumbnails'][0]['url']
        urllib.request.urlretrieve(thumb_url, 'videos/image.jpg')
        return video.title, video.author, video.videoid
    except:
        print('1')

def playlistvids(url):
    import pafy
    import urllib.request
    from youtubesearchpython import VideosSearch
    
    video = pafy.new(url)
    videosSearch = VideosSearch(url, limit = 1)
    thumb_url = videosSearch.result()['result'][0]['thumbnails'][0]['url']
    filename = "videos/" + video.title + ".jpg"
    urllib.request.urlretrieve(thumb_url, filename)
    return video.title, video.author

def nextsong(url):
    import pafy
    import urllib.request
    from youtubesearchpython import VideosSearch
    import random
    
    video = pafy.new(url)
    url_lst = []
    videosSearch = VideosSearch(video.author + "songs" , limit = 10)
    for i in range(10):
        url_lst.append(videosSearch.result()['result'][i]['link'])
    url_new = random.choice(url_lst)
    while url_new == url:
        url_new = random.choice(url_lst)
    return url_new

def deletevid():
    import os
    target = os.getcwd()
    target = os.path.join(target, "videos\\")
    for x in os.listdir(target):
        if x.endswith('.mp4'):
            try:
                os.unlink(target + x)
            except:
                os.remove(target + x)

