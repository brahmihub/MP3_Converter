from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap, QImage
import os
from yt_dlp import YoutubeDL
import re
import urllib.request
import string
path=""
def check_folder():
    global path
    try:
        f=open("path.txt","r")
        path=f.readline().rstrip()
        if path=="" or not(os.path.exists(path)):
            downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
            new_folder_path = os.path.join(downloads_path, "MP3_Converter")
            if not os.path.exists(new_folder_path):
                os.makedirs(new_folder_path)
            f=open("path.txt","w+")
            f.write(new_folder_path)
            f.close()
    except:
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        new_folder_path = os.path.join(downloads_path, "MP3_Converter")
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)
        f=open("path.txt","w+")
        f.write(new_folder_path)
        f.close()
    
    
    
    
    
    
    
def search_click():
    video_url = windows.link.text()

    if video_url == "":
        QMessageBox.critical(windows, "ERROR", "Provide Video URL or Song Name")
    else:
        try:
            output_path, song_title, thumbnail_image = download_audio_stream(video_url, download=False)
            if thumbnail_image:
                # Set the thumbnail image in the QLabel
                pixmap = QPixmap.fromImage(thumbnail_image)
                windows.song_image.setPixmap(pixmap)
                windows.song_image.setScaledContents(True)
            windows.song_name.setText(song_title.replace(".mp3", ""))  # Set only the file name
        except Exception as e:
            QMessageBox.critical(windows, "ERROR", f"Something went wrong: {str(e)} .try again")
            check_folder()
def convert_click():
    video_url = windows.link.text()

    if video_url == "":
        QMessageBox.critical(windows, "ERROR", "Provide Video URL or Song Name")
    else:
        try:
            output_path, song_title, thumbnail_image = download_audio_stream(video_url,download=False)
            output_path, song_title, thumbnail_image = download_audio_stream(video_url)
            if thumbnail_image:
                # Set the thumbnail image in the QLabel
                pixmap = QPixmap.fromImage(thumbnail_image)
                windows.song_image.setPixmap(pixmap)
                windows.song_image.setScaledContents(True)
            windows.song_name.setText(song_title.replace(".mp3", ""))  # Set only the file name
            QMessageBox.information(windows, "Success", f"MP3 file saved: {os.path.join(path, song_title)}.mp3")
        except Exception as e:
            QMessageBox.critical(windows, "ERROR", f"Something went wrong: {str(e)} .try again")
            check_folder()
def download_audio_stream(url, output_path=path, download=True):
    if not url.startswith('http'):
        # Assume it's a search query
        url = f"ytsearch:{url}"

    options = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': f"{os.path.join(path, windows.song_name.text())}.mp3",
        'noplaylist': True,
    }
    with YoutubeDL(options) as ydl:
        info_dict = ydl.extract_info(url, download=download)

        if 'entries' in info_dict:
            # For search results, take the first video
            info_dict = info_dict['entries'][0]

        # Clean the title to remove invalid characters for filenames
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        clean_title = ''.join(c if c in valid_chars else '_' for c in info_dict['title'])

        thumbnail_url = info_dict.get('thumbnail')
        thumbnail_image = None

        if thumbnail_url:
            # Load the thumbnail image directly without saving it to a file
            data = urllib.request.urlopen(thumbnail_url).read()
            image = QImage()
            image.loadFromData(data)
            thumbnail_image = image

    return output_path, clean_title, thumbnail_image
def change_path():
    global path
    folder_path = QFileDialog.getExistingDirectory(windows, "Select Folder")
    if folder_path:
        path=folder_path
        f=open("path.txt","w")
        f.write(path)
        f.close()
def current_path():
    f=open("path.txt","r")
    ch=f.readline().rstrip()
    QMessageBox.information(windows,"Information",f"Current Saving Path is: {ch}")
    f.close()
app = QApplication([])
windows = loadUi("C:/Users/brahm/OneDrive/Desktop/youtube to mp3/interface.ui")
windows.show()
windows.convert.clicked.connect(convert_click)
windows.search.clicked.connect(search_click)
windows.actionChange_Saving_Path.triggered.connect(change_path)
windows.actionCurrent_Saving_Path.triggered.connect(current_path)
check_folder()
windows.setWindowTitle('MP3 Converter')
windows.setWindowIcon(QIcon('sources/icon.png'))
app.exec_()
