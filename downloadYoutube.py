import os
import re
import pafy
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pytube import Playlist
import threading

default_folder = "C:/Users/prapo/Music"

class DownloadThread(threading.Thread):
    def _init__(self):
        super()._init__()
        self.daemon = True
                

# select a folder to save the video
def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)
    return

    # download the video
def download():
    # check if url is playlist or video using regex
    url = url_entry.get()
    # regex to validate youtube url
    regex = (r"(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+")
    # regex to check if youtube link is a playlist
    playlistRegex = (r"(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/playlist(.+)")
    isValidUrl = bool(re.search(regex, url))
    isPlaylist = bool(re.search(playlistRegex, url))
    if (isValidUrl):
        if(isPlaylist):
            DownloadThread(target=download_playlist(url)).start()
        else:
            DownloadThread(target=download_video(url)).start()
    else:
        url_entry.delete(0, tk.END)
        url_entry.insert(0, "Invalid URL")
        print("Invalid URL")
    download_speed.config(text="Download Speed: 0")
    download_size.config(text="Download Size: 0")
    current_download.config(text="Current Download: None")
    progress.config(value=0)
    root.update_idletasks()
    return


def download_video(url):
    print("\n-------------- Downloading Video --------------\n")
    video = pafy.new(url)
    if (audio_button.get() == True):
        best = video.getbestaudio()
        extencion = ".mp3"
    else:
        best = video.getbest()
        extencion = ".mp4"
    current_download.config(text="Current Download: " + video.title)
    root.update_idletasks()
    title = best.title
    if (os.path.exists(os.path.join(folder_path.get(), video.title + ".mp3")) or os.path.exists(os.path.join(folder_path.get(), video.title + ".mp4"))):
        current_download.config(text="File already exists")
        root.update_idletasks()
        print("File already exists")
        return
    
    best.download(callback=updateDownloadSpeedCallback,
                  filepath=folder_path.get() + "/" + title + extencion)
    print("Download Complete")
    
    return;

def download_playlist(url):
    print("\n-------------- Downloading Playlist --------------\n")
    playlist = Playlist(url)
    for video in playlist:
        video = pafy.new(video)
        if (audio_button.get() == True):
            audio = video.getbestaudio()
            extencion = ".mp3"
        else:
            audio = video.getbest()
            extencion = ".mp4"
        current_download.config(text="Current Download: " + video.title)
        root.update_idletasks()
        title = audio.title
        if (os.path.exists(os.path.join(folder_path.get(), video.title + ".mp3")) or os.path.exists(os.path.join(folder_path.get(), video.title + ".mp4"))):
            current_download.config(text="File already exists")
            root.update_idletasks()
            print("File already exists")
            continue
        audio.download(callback=updateDownloadSpeedCallback,
                       filepath=folder_path.get() + "/" + title + extencion)
        print("Download of " + video.title + " Complete")
    print("Download Complete")
    return


def updateDownloadSpeedCallback(total, recvd, ratio, rate, eta):
    recvd_in_mbps = recvd / (1024 * 1024)
    total_in_mbps = total / (1024 * 1024)
    rate_in_mbps = rate / (1024 * 1024)
    
    rate_in_mbps = round(rate_in_mbps, 2)
    recvd_in_mbps = round(recvd_in_mbps, 2)
    total_in_mbps = round(total_in_mbps, 2)

    # update download speed and size
    progress.config(value=(recvd * 100) / total)
    # only show 2 decimal places
    download_speed.config(text= "Download Speed: " + str(rate_in_mbps) + " mbps")
    download_size.config(text="Download Size: " + str(recvd_in_mbps) + "MBs / " + str(total_in_mbps) + " MBs")
    root.update_idletasks()


def on_closing():
    root.destroy()
    return


# Tkinter GUI

root = tk.Tk()
root.geometry("800x500")
# title of the root
root.title("Youtube Downloader")

# select video url
url = tk.StringVar()
url_label = ttk.Label(root, text="Video URL: ", font=("Arial", 10))
url_label.place(x=20, y=20)
url_entry = ttk.Entry(root, width=100, textvariable=url)
url_entry.place(x=100, y=20)

# button to enable or disable audio recording
audio_button = tk.BooleanVar()
audio_check = ttk.Checkbutton(root, text="Audio Only", variable=audio_button)
audio_check.place(x=100, y=80)
audio_button.set(True)

# select folder to save video
folder_path = tk.StringVar()
folder_label = ttk.Label(root, text="Folder Path: ", font=("Arial", 10))
folder_label.place(x=20, y=50)
folder_entry = ttk.Entry(root, width=100, textvariable=folder_path)
folder_entry.place(x=100, y=50)
folder_path.set(default_folder)

# select folder button
folder_button = ttk.Button(root, text="Select Folder", command=lambda: DownloadThread(target=select_folder).start())
folder_button.place(x=20, y=80)

# download button
download_button = ttk.Button(root, text="Download", command=lambda: DownloadThread(target=download).start())
download_button.place(x=20, y=110)

#current music downloaded
current_download = ttk.Label(
    root, text="Current Download: None", font=("Arial", 10))
current_download.place(x=100, y=80)

# progress of download bar
progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress.place(x=20, y=170)

# progress to show download speed and total size
download_speed = ttk.Label(root, text="Download Speed: 0", font=("Arial", 10))
download_speed.place(x=20, y=200)
download_size = ttk.Label(root, text="Download Size: 0", font=("Arial", 10))
download_size.place(x=20, y=230)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
