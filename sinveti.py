import sys
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QFileDialog, QSlider
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PIL import Image
import Core.records as r
import pickle as p
import Core.datam as datam
import Core.yt_home as yt
import Core.lyrics as lyrics
import webbrowser

img, profile = '', ''
user = ''
txt = ''
url = ''
url_lst = []
totalduration = 0
autovar = False

class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("UI/welcome_screen.ui",self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotocreate)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotocreate(self):
        create = CreateAccScreen()
        widget.addWidget(create)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("UI/login_screen.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login.clicked.connect(self.loginfunction)
        self.back.clicked.connect(self.backfunction)
        self.reset.clicked.connect(self.gotoreset)

    def backfunction(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoreset(self):
        reset = ResetScreen()
        widget.addWidget(reset)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def loginfunction(self):
        global user
        user = self.userfield.text()
        password = self.passwordfield.text()

        if len(user)==0 or len(password)==0:
            self.error.setText("Please input all fields.")

        else:
            found = False
            with open('Files/entries.dat', 'rb') as file:
                try:
                    while True:
                        record = p.load(file)
                        if record != {}:
                            if record['user'] == user:
                                result = record['password']
                                found = True
                                break
                        else:
                            pass
                except EOFError:
                    file.close()
            if found == False:
                result = "Not_found"
            if result == password:
                self.error.setText("")
                self.success.setText("Please wait. Loading Home Screen....")
                try:
                    global img
                    global profile
                    img, profile = r.image(user)
                    yt.deletevid()
                    home = HomeScreen()
                    widget.addWidget(home)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                except:
                    nowifi = NoWifiScreen()
                    widget.addWidget(nowifi)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                self.error.setText("Invalid username or password")

class CreateAccScreen(QDialog):
    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi("UI/signup_screen.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)
        self.back.clicked.connect(self.backfunction)

    def backfunction(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def signupfunction(self):
        global user
        user = self.userfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user)==0 or len(password)==0 or len(confirmpassword)==0:
            self.Error.setText("Please fill in all inputs.")

        elif password!=confirmpassword:
            self.Error.setText("Passwords do not match.")
        else:
            with open('Files/entries.dat', 'ab') as file:
                data = {'user':user, 'password':password}
                p.dump(data, file)
            file.close()
            self.success.setText("Please wait. Loading Home Screen....")
            try:
                global img
                global profile
                img = 'placeholder.png'
                profile = 'profile.png'
                home = HomeScreen()
                widget.addWidget(home)
                widget.setCurrentIndex(widget.currentIndex()+1)
            except:
                nowifi = NoWifiScreen()
                widget.addWidget(nowifi)
                widget.setCurrentIndex(widget.currentIndex()+1)

class HomeScreen(QDialog):
    def __init__(self):
        super(HomeScreen, self).__init__()
        loadUi("UI/home.ui",self)
        global profile
        self.home_label.setPixmap(QPixmap('home_button.png'))
        self.search_label.setPixmap(QPixmap('search_button.jpg'))
        self.profile_label.setPixmap(QPixmap(profile))
        self.playlist_label.setPixmap(QPixmap('music_playlist.png'))
        self.reload_label.setPixmap(QPixmap('reload.png'))
        self.profile.clicked.connect(self.gotoprofile)
        self.playlist.clicked.connect(self.gotoplaylist)
        self.video.clicked.connect(self.gotovideo1)
        self.video_2.clicked.connect(self.gotovideo2)
        self.video_3.clicked.connect(self.gotovideo3)
        self.video_4.clicked.connect(self.gotovideo4)
        self.video_5.clicked.connect(self.gotovideo5)
        self.video_6.clicked.connect(self.gotovideo6)
        self.search.clicked.connect(self.gotosearch)
        self.reloadbtn.clicked.connect(self.gotohome)
        global url_lst
        name_lst, url_lst = yt.youtube_home()
        self.vid1.setPixmap(QPixmap("Thumbnails/0.jpg"))
        self.vid2.setPixmap(QPixmap("Thumbnails/1.jpg"))
        self.vid3.setPixmap(QPixmap("Thumbnails/2.jpg"))
        self.vid4.setPixmap(QPixmap("Thumbnails/3.jpg"))
        self.vid5.setPixmap(QPixmap("Thumbnails/4.jpg"))
        self.vid6.setPixmap(QPixmap("Thumbnails/5.jpg"))

    def gotohome(self):
        try:
            home = HomeScreen()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)


    def gotoprofile(self):
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoplaylist(self):
        playlist = PlaylistScreen()
        widget.addWidget(playlist)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo1(self):
        try:
            global url
            global url_lst
            url = url_lst[0]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo2(self):
        try:
            global url
            global url_lst
            url = url_lst[1]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo3(self):
        try:
            global url
            global url_lst
            url = url_lst[2]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo4(self):
        try:
            global url
            global url_lst
            url = url_lst[3]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo5(self):
        try:
            global url
            global url_lst
            url = url_lst[4]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo6(self):
        try:
            global url
            global url_lst
            url = url_lst[5]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosearch(self):
        global txt
        txt = self.searchtxt.text()

        if txt != '':
            if txt == ":about":
                try:
                    about = AboutScreen()
                    widget.addWidget(about)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                except:
                    nowifi = NoWifiScreen()
                    widget.addWidget(nowifi)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            elif txt == ":source-code":
                try:
                    dev = DevMode()
                    widget.addWidget(dev)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                except:
                    nowifi = NoWifiScreen()
                    widget.addWidget(nowifi)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            elif txt == ":dev-mode":
                try:
                    auth = AuthScreen()
                    widget.addWidget(auth)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                except:
                    nowifi = NoWifiScreen()
                    widget.addWidget(nowifi)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            elif txt == ":exit":
                sys.exit()
            else:
                try:
                    search = SearchScreen()
                    widget.addWidget(search)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                except:
                    nowifi = NoWifiScreen()
                    widget.addWidget(nowifi)
                    widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            print("Invalid Search")

class ProfileScreen(QDialog):
    def __init__(self):
        super(ProfileScreen, self).__init__()
        loadUi("UI/profile_page.ui",self)
        global img
        global profile
        self.placeholder.setPixmap(QPixmap(img))
        self.home_label.setPixmap(QPixmap('home_button.png'))
        self.search_label.setPixmap(QPixmap('search_button.jpg'))
        self.profile_label.setPixmap(QPixmap(profile))
        self.playlist_label.setPixmap(QPixmap('music_playlist.png'))
        self.playlist.clicked.connect(self.gotoplaylist)
        self.save.clicked.connect(self.savefunc)
        self.Home.clicked.connect(self.gotohome)
        self.change.clicked.connect(self.changefunc)
        self.search.clicked.connect(self.gotosearch)
        self.logout.clicked.connect(self.logoutfunc)
        global user
        self.userfield.setText(user)

    def logoutfunc(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def gotoplaylist(self):
        playlist = PlaylistScreen()
        widget.addWidget(playlist)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def savefunc(self):
        self.success.setText("Profile Saved Successfully!!")

    def gotohome(self):
        try:
            home = HomeScreen()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def changefunc(self):
        global img
        global profile
        global user
        filename, _ = QFileDialog.getOpenFileName(self, "Upload Profile Photo")
        if filename != '':
            img = filename
            profile = img
            r.savefunc(img, profile, user)
            im = Image.open(img)
            img = im.resize((250,250))
            img.save('im_250.png')
            img = 'im_250.png'
            self.placeholder.setPixmap(QPixmap(img))
            profile = im.resize((101,91))
            profile.save('im_101.png')
            profile = 'im_101.png'
        if filename[-15:] == "placeholder.png":
            profile = 'profile.png'
        self.profile_label.setPixmap(QPixmap(profile))

    def gotosearch(self):
        global txt
        txt = self.searchtxt.text()

        try:
            if txt != '':
                if txt == ":about":
                    about = AboutScreen()
                    widget.addWidget(about)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":source-code":
                    dev = DevMode()
                    widget.addWidget(dev)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":dev-mode":
                    auth = AuthScreen()
                    widget.addWidget(auth)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":exit":
                    sys.exit()
                else:
                    search = SearchScreen()
                    widget.addWidget(search)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                print("Invalid Search")
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

class PlaylistScreen(QDialog):
    def __init__(self):
        super(PlaylistScreen, self).__init__()
        loadUi("UI/playlist_page.ui",self)
        global profile
        self.home_label.setPixmap(QPixmap('home_button.png'))
        self.search_label.setPixmap(QPixmap('search_button.jpg'))
        self.profile_label.setPixmap(QPixmap(profile))
        self.playlist_label.setPixmap(QPixmap('music_playlist.png'))
        self.profile.clicked.connect(self.gotoprofile)
        self.Home.clicked.connect(self.gotohome)
        self.search.clicked.connect(self.gotosearch)
        self.btn1.setEnabled(False)
        self.btn2.setEnabled(False)
        self.btn3.setEnabled(False)
        self.btn4.setEnabled(False)
        self.btn5.setEnabled(False)
        self.btn6.setEnabled(False)
        self.btn7.setEnabled(False)
        with open('Files/playlist.dat', 'rb') as file:
            try:
                global url_lst
                url_lst = []
                i = 0
                while True:
                    global user
                    data = p.load(file)
                    i += 1
                    img_label = 'vid'+ str(i)
                    if data['user'] == user:
                        self.capacity.setText(str(i) + '/7')
                        url_lst.append(data['url'])
                        filename = "videos/" + data["title"] + ".jpg"
                        if img_label == "vid1":
                            self.vid1.setPixmap(QPixmap(filename))
                            self.vid1_label.setText(data["title"])
                            self.btn1.setEnabled(True)
                            self.vid1_label.setStyleSheet("background-color: white; font: 20pt MS Shell Dlg 2;")
                        elif img_label == "vid2":
                            self.vid2.setPixmap(QPixmap(filename))
                            self.vid2_label.setText(data["title"])
                            self.btn2.setEnabled(True)
                            self.vid2_label.setStyleSheet("background-color: white; font: 20pt MS Shell Dlg 2;")
                        elif img_label == "vid3":
                            self.vid3.setPixmap(QPixmap(filename))
                            self.vid3_label.setText(data["title"])
                            self.btn3.setEnabled(True)
                            self.vid3_label.setStyleSheet("background-color: white; font: 20pt MS Shell Dlg 2;")
                        elif img_label == "vid4":
                            self.vid4.setPixmap(QPixmap(filename))
                            self.vid4_label.setText(data["title"])
                            self.btn4.setEnabled(True)
                            self.vid4_label.setStyleSheet("background-color: white; font: 20pt MS Shell Dlg 2;")
                        elif img_label == "vid5":
                            self.vid5.setPixmap(QPixmap(filename))
                            self.vid5_label.setText(data["title"])
                            self.btn5.setEnabled(True)
                            self.vid5_label.setStyleSheet("background-color: white; font: 20pt MS Shell Dlg 2;")
                        elif img_label == "vid6":
                            self.vid6.setPixmap(QPixmap(filename))
                            self.vid6_label.setText(data["title"])
                            self.btn6.setEnabled(True)
                            self.vid6_label.setStyleSheet("background-color: white; font: 20pt MS Shell Dlg 2;")
                        elif img_label == "vid7":
                            self.vid7.setPixmap(QPixmap(filename))
                            self.vid7_label.setText(data["title"])
                            self.btn7.setEnabled(True)
                            self.vid7_label.setStyleSheet("background-color: white; font: 20pt MS Shell Dlg 2;")
                    else:
                        i -= 1
            except:
                file.close()
        self.btn1.clicked.connect(self.gotovideo1)
        self.btn2.clicked.connect(self.gotovideo2)
        self.btn3.clicked.connect(self.gotovideo3)
        self.btn4.clicked.connect(self.gotovideo4)
        self.btn5.clicked.connect(self.gotovideo5)
        self.btn6.clicked.connect(self.gotovideo6)
        self.btn7.clicked.connect(self.gotovideo7)

    def gotovideo1(self):
        try:
            global url
            global url_lst
            url = url_lst[0]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo2(self):
        try:
            global url
            global url_lst
            url = url_lst[1]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo3(self):
        try:
            global url
            global url_lst
            url = url_lst[2]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo4(self):
        try:
            global url
            global url_lst
            url = url_lst[3]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo5(self):
        try:
            global url
            global url_lst
            url = url_lst[4]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo6(self):
        try:
            global url
            global url_lst
            url = url_lst[5]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo7(self):
        try:
            global url
            global url_lst
            url = url_lst[6]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoprofile(self):
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotohome(self):
        try:
            home = HomeScreen()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosearch(self):
        global txt
        txt = self.searchtxt.text()

        try:
            if txt != '':
                if txt == ":about":
                    about = AboutScreen()
                    widget.addWidget(about)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":source-code":
                    dev = DevMode()
                    widget.addWidget(dev)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":dev-mode":
                    auth = AuthScreen()
                    widget.addWidget(auth)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":exit":
                    sys.exit()
                else:
                    search = SearchScreen()
                    widget.addWidget(search)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                print("Invalid Search")
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

class VideoScreen(QDialog):
    def __init__(self):
        super(VideoScreen, self).__init__()
        loadUi("UI/video_page.ui",self)
        global profile
        self.home_label.setPixmap(QPixmap('home_button.png'))
        self.search_label.setPixmap(QPixmap('search_button.jpg'))
        self.profile_label.setPixmap(QPixmap(profile))
        self.playlist_label.setPixmap(QPixmap('music_playlist.png'))
        self.play_label.setPixmap(QPixmap('playbtn.jfif'))
        self.pause_label.setPixmap(QPixmap('pausebtn.png'))
        self.fav_label.setPixmap(QPixmap('heartbtn.png'))
        self.next_label.setPixmap(QPixmap('nextbtn.jpg'))
        self.up_label.setPixmap(QPixmap('upbtn.png'))
        self.down_label.setPixmap(QPixmap('downbtn.jfif'))
        self.vid_tick.setPixmap(QPixmap('tickmark.png'))
        self.aud_tick.setPixmap(QPixmap('tickmark.png'))
        self.tick.setPixmap(QPixmap('tickmark.png'))
        self.vid_tick.setHidden(True)
        self.tick.setHidden(True)
        self.profile.clicked.connect(self.gotoprofile)
        self.Home.clicked.connect(self.gotohome)
        self.playlist.clicked.connect(self.gotoplaylist)
        self.search.clicked.connect(self.gotosearch)
        self.play.clicked.connect(self.playaudio)
        self.pause.clicked.connect(self.pauseaudio)
        self.fav.clicked.connect(self.favaudio)
        self.next.clicked.connect(self.nextaudio)
        self.up.clicked.connect(self.volumeup)
        self.down.clicked.connect(self.volumedown)
        self.vid.toggled.connect(self.vidfunc)
        self.aud.toggled.connect(self.audfunc)
        self.loop.toggled.connect(self.loopvid)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setHidden(True)
        self.vid.setChecked(False)
        self.aud.setChecked(False)
        self.loop.setChecked(False)
        global url
        title, author, vidid = yt.viddata(url)
        self.name.setText(title + '\n' + author)
        im = Image.open('videos/image.jpg')
        image = im.resize((630,380))
        image.save('im_630.png')
        image = 'im_630.png'
        self.image.setPixmap(QPixmap(image))
        txt = lyrics.songlyrics(url)
        self.lyrics.setText(txt)
        self.mediaPlayer = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile('videos/' + vidid + '.mp4')))
        self.mediaPlayer.setVideoOutput(self.video_player)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

    def audfunc(self):
        if self.aud.isChecked():
            self.vid.setChecked(False)
            self.image.setHidden(False)
            self.vid_tick.setHidden(True)
            self.aud_tick.setHidden(False)
            self.positionSlider.setHidden(True)
        else:
            self.aud.setChecked(False)
            self.image.setHidden(True)
            self.vid_tick.setHidden(False)
            self.aud_tick.setHidden(True)
            self.positionSlider.setHidden(False)

    def vidfunc(self):
        if self.vid.isChecked():
            self.aud.setChecked(False)
            self.image.setHidden(True)
            self.vid_tick.setHidden(False)
            self.aud_tick.setHidden(True)
            self.positionSlider.setHidden(False)
        else:
            self.vid.setChecked(False)
            self.image.setHidden(False)
            self.vid_tick.setHidden(True)
            self.aud_tick.setHidden(False)
            self.positionSlider.setHidden(True)
    
    def playaudio(self):
        self.mediaPlayer.play()
        self.videostate.setText("Video Playing")

    def pauseaudio(self):
        self.mediaPlayer.pause()
        self.videostate.setText("Video Paused")

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        global totalduration
        totalduration = duration
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def loopvid(self):
        if True:
            if self.loop.isChecked():
                self.tick.setHidden(False)
                self.positionSlider.valueChanged.connect(self.valuechange)
            else:
                 self.tick.setHidden(True)

    def valuechange(self):
        global totalduration
        value = self.positionSlider.value()
        if value == totalduration:
            if self.loop.isChecked():
                self.mediaPlayer.play()
        else:
            self.pause.clicked.connect(self.pauseaudio)

    def favaudio(self):
        lst = []
        with open('Files/playlist.dat', 'rb') as file:
            try:
                while True:
                    content = p.load(file)
                    lst.append(content)
            except:
                file.close()
        with open('Files/playlist.dat', 'ab') as file:
            global url
            global user
            title, author = yt.playlistvids(url)
            data = {'url':url, 'title':title, 'user':user}
            if data not in lst:
                p.dump(data, file)
                self.playfav.setText("Added to playlist")
            else:
                with open('Files/playlist.dat', 'wb') as f:
                    for line in lst:
                        if line != data:
                            p.dump(line, f)
                        else:
                            self.playfav.setText("Removed from Playlist")
        file.close()

    def nextaudio(self):
        self.mediaPlayer.pause()
        global url
        new_url = yt.nextsong(url)
        url = new_url
        try:
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def volumeup(self):
        currentVolume = self.mediaPlayer.volume() 
        self.mediaPlayer.setVolume(currentVolume + 10)

    def volumedown(self):
        currentVolume = self.mediaPlayer.volume() 
        self.mediaPlayer.setVolume(currentVolume - 10)

    def gotoprofile(self):
        self.mediaPlayer.pause()
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotohome(self):
        try:
            self.mediaPlayer.pause()
            home = HomeScreen()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoplaylist(self):
        try:
            self.mediaPlayer.pause()
            playlist = PlaylistScreen()
            widget.addWidget(playlist)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosearch(self):
        global url
        global txt
        txt = self.searchtxt.text()

        try:
            if txt != '':
                if txt == ":about":
                    self.mediaPlayer.pause()
                    about = AboutScreen()
                    widget.addWidget(about)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":source-code":
                    self.mediaPlayer.pause()
                    dev = DevMode()
                    widget.addWidget(dev)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":dev-mode":
                    self.mediaPlayer.pause()
                    auth = AuthScreen()
                    widget.addWidget(auth)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":exit":
                    sys.exit()
                elif txt == ":yt":
                    webbrowser.open_new_tab(url)
                else:
                    self.mediaPlayer.pause()
                    search = SearchScreen()
                    widget.addWidget(search)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                print("Invalid Search")
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

class ResetScreen(QDialog):
    def __init__(self):
        super(ResetScreen, self).__init__()
        loadUi("UI/reset_screen.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirmpasswordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.reset.clicked.connect(self.resetfunction)
        self.back.clicked.connect(self.backfunction)

    def backfunction(self):
        welcome = WelcomeScreen()
        widget.addWidget(welcome)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
    def resetfunction(self):
        prev = self.prevfield.text()
        user = self.userfield.text()
        password = self.passwordfield.text()
        confirmpassword = self.confirmpasswordfield.text()

        if len(user)==0 or len(password)==0 or len(confirmpassword)==0 or len(prev)==0 :
            self.Error.setText("Please fill in all inputs.")

        elif password!=confirmpassword:
            self.Error.setText("Passwords do not match.")
        else:
            datam.reset(prev, user, password)
            
            login = LoginScreen()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)

class AboutScreen(QDialog):
    def __init__(self):
        super(AboutScreen, self).__init__()
        loadUi("UI/about.ui",self)
        global profile
        self.home_label.setPixmap(QPixmap('home_button.png'))
        self.search_label.setPixmap(QPixmap('search_button.jpg'))
        self.profile_label.setPixmap(QPixmap(profile))
        self.playlist_label.setPixmap(QPixmap('music_playlist.png'))
        self.logo.setPixmap(QPixmap('logo.jfif'))
        self.profile.clicked.connect(self.gotoprofile)
        self.Home.clicked.connect(self.gotohome)
        self.playlist.clicked.connect(self.gotoplaylist)
        self.search.clicked.connect(self.gotosearch)

    def gotoprofile(self):
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotohome(self):
        try:
            home = HomeScreen()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)


    def gotoplaylist(self):
        playlist = PlaylistScreen()
        widget.addWidget(playlist)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosearch(self):
        global txt
        txt = self.searchtxt.text()

        try:
            if txt != '':
                if txt == ":about":
                    pass
                elif txt == ":source-code":
                    dev = DevMode()
                    widget.addWidget(dev)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":dev-mode":
                    auth = AuthScreen()
                    widget.addWidget(auth)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":exit":
                    sys.exit()
                else:
                    search = SearchScreen()
                    widget.addWidget(search)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                print("Invalid Search")
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

class DevMode(QDialog):
    def __init__(self):
        super(DevMode, self).__init__()
        loadUi("UI/dev_mode.ui",self)
        global profile
        self.home_label.setPixmap(QPixmap('home_button.png'))
        self.search_label.setPixmap(QPixmap('search_button.jpg'))
        self.profile_label.setPixmap(QPixmap(profile))
        self.playlist_label.setPixmap(QPixmap('music_playlist.png'))
        with open('Files/main.py', 'r') as file:
            content = file.read()
            self.code.setText(content)
        with open('Files/records.py', 'r') as file:
            content = file.read()
            self.code_2.setText(content)
        with open('Files/yt_home.py', 'r') as file:
            content = file.read()
            self.code_3.setText(content)
        with open('Files/datam.py', 'r') as file:
            content = file.read()
            self.code_4.setText(content)
        with open('Files/lyrics.py', 'r') as file:
            content = file.read()
            self.code_5.setText(content)
        self.profile.clicked.connect(self.gotoprofile)
        self.Home.clicked.connect(self.gotohome)
        self.playlist.clicked.connect(self.gotoplaylist)
        self.search.clicked.connect(self.gotosearch)

    def gotoprofile(self):
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotohome(self):
        try:
            home = HomeScreen()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)


    def gotoplaylist(self):
        playlist = PlaylistScreen()
        widget.addWidget(playlist)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosearch(self):
        global txt
        txt = self.searchtxt.text()

        try:
            if txt != '':
                if txt == ":about":
                    about = AboutScreen()
                    widget.addWidget(about)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":source-code":
                    pass
                elif txt == ":dev-mode":
                    auth = AuthScreen()
                    widget.addWidget(auth)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":exit":
                    sys.exit()
                else:
                    search = SearchScreen()
                    widget.addWidget(search)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                print("Invalid Search")
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

class SearchScreen(QDialog):
    def __init__(self):
        super(SearchScreen, self).__init__()
        loadUi("UI/search.ui",self)
        global profile
        self.home_label.setPixmap(QPixmap('home_button.png'))
        self.search_label.setPixmap(QPixmap('search_button.jpg'))
        self.profile_label.setPixmap(QPixmap(profile))
        self.playlist_label.setPixmap(QPixmap('music_playlist.png'))
        self.profile.clicked.connect(self.gotoprofile)
        self.Home.clicked.connect(self.gotohome)
        self.playlist.clicked.connect(self.gotoplaylist)
        self.search.clicked.connect(self.gotosearch)
        global txt
        self.searchtxt.setText(txt)
        global url_lst
        name_lst, url_lst = yt.yt_search(txt)
        self.vid1_label.setText('  ' + name_lst[0])
        self.vid2_label.setText('  ' + name_lst[1])
        self.vid3_label.setText('  ' + name_lst[2])
        self.vid4_label.setText('  ' + name_lst[3])
        self.vid5_label.setText('  ' + name_lst[4])
        self.vid6_label.setText('  ' + name_lst[5])
        self.vid7_label.setText('  ' + name_lst[6])
        self.vid8_label.setText('  ' + name_lst[7])
        self.vid1.setPixmap(QPixmap("search_Thumbnails/0.jpg"))
        self.vid2.setPixmap(QPixmap("search_Thumbnails/1.jpg"))
        self.vid3.setPixmap(QPixmap("search_Thumbnails/2.jpg"))
        self.vid4.setPixmap(QPixmap("search_Thumbnails/3.jpg"))
        self.vid5.setPixmap(QPixmap("search_Thumbnails/4.jpg"))
        self.vid6.setPixmap(QPixmap("search_Thumbnails/5.jpg"))
        self.vid7.setPixmap(QPixmap("search_Thumbnails/6.jpg"))
        self.vid8.setPixmap(QPixmap("search_Thumbnails/7.jpg"))
        self.btn1.clicked.connect(self.gotovideo1)
        self.btn2.clicked.connect(self.gotovideo2)
        self.btn3.clicked.connect(self.gotovideo3)
        self.btn4.clicked.connect(self.gotovideo4)
        self.btn5.clicked.connect(self.gotovideo5)
        self.btn6.clicked.connect(self.gotovideo6)
        self.btn7.clicked.connect(self.gotovideo7)
        self.btn8.clicked.connect(self.gotovideo8)

    def gotovideo1(self):
        try:
            global url
            global url_lst
            url = url_lst[0]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo2(self):
        try:
            global url
            global url_lst
            url = url_lst[1]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo3(self):
        try:
            global url
            global url_lst
            url = url_lst[2]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo4(self):
        try:
            global url
            global url_lst
            url = url_lst[3]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo5(self):
        try:
            global url
            global url_lst
            url = url_lst[4]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo6(self):
        try:
            global url
            global url_lst
            url = url_lst[5]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo7(self):
        try:
            global url
            global url_lst
            url = url_lst[6]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotovideo8(self):
        try:
            global url
            global url_lst
            url = url_lst[7]
            video = VideoScreen()
            widget.addWidget(video)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoprofile(self):
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotohome(self):
        try:
            home = HomeScreen()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoplaylist(self):
        playlist = PlaylistScreen()
        widget.addWidget(playlist)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosearch(self):
        global txt
        txt = self.searchtxt.text()
        try:
            if txt != '':
                if txt == ":about":
                    about = AboutScreen()
                    widget.addWidget(about)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":source-code":
                    dev = DevMode()
                    widget.addWidget(dev)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":dev-mode":
                    auth = AuthScreen()
                    widget.addWidget(auth)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":exit":
                    sys.exit()
                else:
                    search = SearchScreen()
                    widget.addWidget(search)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                print("Invalid Search")
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

class DevScreen(QDialog):
    def __init__(self):
        super(DevScreen, self).__init__()
        loadUi("UI/dev.ui",self)
        global profile
        self.home_label.setPixmap(QPixmap('home_button.png'))
        self.search_label.setPixmap(QPixmap('search_button.jpg'))
        self.profile_label.setPixmap(QPixmap(profile))
        self.playlist_label.setPixmap(QPixmap('music_playlist.png'))
        self.profile.clicked.connect(self.gotoprofile)
        self.Home.clicked.connect(self.gotohome)
        self.playlist.clicked.connect(self.gotoplaylist)
        self.search.clicked.connect(self.gotosearch)
        self.delete_2.clicked.connect(self.confirmation)
        self.passwd.clicked.connect(self.getpasswd)
        self.yes.clicked.connect(self.deleteuser)
        self.no.clicked.connect(self.nofunc)
        self.yes.setHidden(True)
        self.no.setHidden(True)
        self.conflabel.setHidden(True)
        self.yes.setEnabled(False)
        self.no.setEnabled(False)

    def deleteuser(self):
        user = self.username.text()
        text = datam.delete(user)
        self.yes.setHidden(True)
        self.no.setHidden(True)
        self.conflabel.setHidden(False)
        self.yes.setEnabled(False)
        self.no.setEnabled(False)
        self.conflabel.setText(user + text)

    def confirmation(self):
        user = self.username.text()
        self.conflabel.setText("Are you sure you want to delete " + user + " - ")
        self.conflabel.setHidden(False)
        self.yes.setHidden(False)
        self.no.setHidden(False)
        self.yes.setEnabled(True)
        self.no.setEnabled(True)

    def nofunc(self):
        self.yes.setHidden(True)
        self.no.setHidden(True)
        self.conflabel.setHidden(True)
        self.yes.setEnabled(False)
        self.no.setEnabled(False)

    def getpasswd(self):
        user = self.username.text()
        if user != '':
            found = False
            with open('Files/entries.dat', 'rb') as file:
                try:
                    while True:
                        record = p.load(file)
                        if record != {}:
                            if record['user'] == user:
                                result = record['password']
                                found = True
                                break
                except EOFError:
                    file.close()
            if found == False:
                result = "Username not present"
        else:
            result = ''
            pass
        self.password.setText(result)

    def gotoprofile(self):
        profile = ProfileScreen()
        widget.addWidget(profile)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotohome(self):
        try:
            home = HomeScreen()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

    def gotoplaylist(self):
        playlist = PlaylistScreen()
        widget.addWidget(playlist)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosearch(self):
        global txt
        txt = self.searchtxt.text()
        try:
            if txt != '':
                if txt == ":about":
                    about = AboutScreen()
                    widget.addWidget(about)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":source-code":
                    dev = DevMode()
                    widget.addWidget(dev)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                elif txt == ":dev-mode":
                    pass
                elif txt == ":exit":
                    sys.exit()
                else:
                    search = SearchScreen()
                    widget.addWidget(search)
                    widget.setCurrentIndex(widget.currentIndex()+1)
            else:
                print("Invalid Search")
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

class NoWifiScreen(QDialog):
    def __init__(self):
        super(NoWifiScreen, self).__init__()
        loadUi("UI/no_internet.ui",self)
        self.img.setPixmap(QPixmap('nwimg.jfif'))
        self.rbtn.clicked.connect(self.reload)

    def reload(self):
        try:
            home = HomeScreen()
            widget.addWidget(home)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except:
            nowifi = NoWifiScreen()
            widget.addWidget(nowifi)
            widget.setCurrentIndex(widget.currentIndex()+1)

class AuthScreen(QDialog):
    def __init__(self):
        super(AuthScreen, self).__init__()
        loadUi("UI/auth.ui",self)
        self.passwordfield.setEchoMode(QtWidgets.QLineEdit.Password)
        self.authbtn.clicked.connect(self.authfunction)

    def authfunction(self):
        user = self.userfield.text()
        password = self.passwordfield.text()

        if len(user)==0 or len(password)==0:
            self.error.setText("Please input all fields.")

        else:
            found = False
            with open('Files/entries.dat', 'rb') as file:
                try:
                    while True:
                        record = p.load(file)
                        if record != {}:
                            if record['user'] == user:
                                result = record['password']
                                found = True
                                break
                        else:
                            pass
                except EOFError:
                    file.close()
            if found == False:
                result = "Denied"
            if user == "Advay" or user == "Khushi" or user == "Meet":
                if result == password:
                    self.error.setText("")
                    devscr = DevScreen()
                    widget.addWidget(devscr)
                    widget.setCurrentIndex(widget.currentIndex()+1)
                else:
                    self.error.setText("Incorrect Password - Access Denied")
            else:
                self.error.setText("Access Denied")

# main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.setWindowTitle("Sinveti Music Player")
widget.setWindowIcon(QIcon('logo.jfif'))
widget.show()
try:
    sys.exit(app.exec_())
except:
    pass
