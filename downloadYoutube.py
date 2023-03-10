import os
import re
import pafy
import tkinter as tk
import base64
from tkinter import ttk
from tkinter import filedialog
from pytube import Playlist
from threading import Thread
import threading

default_folder = "C:/Users/prapo/Music"

# select a folder to save the video
def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)
    return

    # download the video
def download(event):
    event = threading.Event()
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
            download_playlist(url)
        else:
            download_video(url)
    else:
        url_entry.delete(0, tk.END)
        url_entry.insert(0, "Invalid URL")
        print("Invalid URL")
    download_speed.config(text="Download Speed: 0")
    download_size.config(text="Download Size: 0")
    current_download.config(text="Current Download: None")
    progress.config(value=0)
    root.update_idletasks()
    event.set()
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
    rate_in_mbps = rate / (1024)
    
    rate_in_mbps = round(rate_in_mbps, 2)
    recvd_in_mbps = round(recvd_in_mbps, 2)
    total_in_mbps = round(total_in_mbps, 2)

    # update download speed and size
    progress.config(value=(recvd * 100) / total)
    # only show 2 decimal places
    download_speed.config(text= "Download Speed: " + str(rate_in_mbps) + " mbps")
    download_size.config(text="Download Size: " + str(recvd_in_mbps) + "MBs / " + str(total_in_mbps) + " MBs")
    root.update_idletasks()

def stop(event):
    # stop all threads
    print("Stopping all threads")
    for thread in threading.enumerate():
        if (thread.name == "downloadThread"):
            thread._delete()
    return
    

def on_closing():
    root.destroy()
    return


# Tkinter GUI
event = threading.Event()
root = tk.Tk()
root.geometry("800x500")
# title of the root
root.title("Youtube Downloader")
icon = "AAABAAEAICAAAAEAIACoEAAAFgAAACgAAAAgAAAAQAAAAAEAIAAAAAAAABAAACMuAAAjLgAAAAAAAAAAAAD//////////////////////////////////////////////////////Pz8/+/v7//f39//09PT/83Nzf/Kysr/ysrK/8zMzP/S0tL/39/f//Dw8P/8/Pz/////////////////////////////////////////////////////////////////////////////////////////////////+fn5/+Tk5P/S0tL/09PT/+Dg3v/r6+n/8fHu//Pz8f/z8/H/8PDu/+fn5f/Z2dj/zMzM/87Ozv/k5OT/+vr6/////////////////////////////////////////////////////////////////////////////f39/+jo6P/R0dH/39/e//X08v/v7/X/0NHs/6yv4v+Slt3/h4vb/4iM0f+Ymsv/t7nZ/9zd6v/19fb/7u7s/9LS0f/Ly8v/6enp//7+/v////////////////////////////////////////////////////////////n5+f/a2tr/2trZ//b29P/f4PD/k5fc/1BW0/8tNdT/ICnX/xwm2f8aI83/Fh2t/xYdpP8cI6T/MDao/2Bltv+vsdX/8PD0/+3t7P/Kysr/2NjY//r6+v/////////////////////////////////////////////////39/f/1tbW/+fn5v/x8fb/m57d/z1F0/8dJ9j/HCbb/x4o2/8fKdz/HSfP/xkhr/8YH6b/GB+n/xgfp/8WHaf/FBul/x0jpP9UWbH/wcPd//j49//T09P/0NDQ//j4+P//////////////////////////////////////+fn5/9fX1//t7ez/4eLx/2dt1P8hKtb/HSfb/x8p2/8fKdv/Hync/x0nz/8ZIa//GB+m/xgfp/8YH6f/GB+n/xgfp/8YH6f/GB+n/xUcpv8pL6b/lZfJ//X19//Y2Nf/0NDQ//r6+v////////////////////////////39/f/b29v/6urp/93e7v9UW9L/HCbZ/x8p2/8fKdv/Hynb/x8p3P8dJ8//GSGv/xgfpv8YH6f/GB+n/xgfp/8YH6f/GB+n/xgfp/8YH6f/GB+n/xYdp/8dI6T/hYjD//X19//T09P/2NjY//7+/v//////////////////////5+fn/+Hh4f/p6fH/XGLQ/xwm2f8fKdv/Hynb/x8p2/8fKdz/HSfP/xkhr/8YH6b/GB+n/xgfp/8YH6f/GB+n/xgfp/8YH6f/GB+n/xgfp/8YH6f/GB+n/xcep/8dI6T/lZfJ//f29v/Kysr/6Ojo//////////////////j4+P/Z2dn/9vb1/4KH0f8eJ9b/Hynb/x8p2/8fKdv/Hync/x0nz/8ZIK//Fx6m/xcep/8XHqf/Fx6n/xcep/8XHqf/Fx6n/xgfp/8YH6f/GB+n/xgfp/8YH6f/GB+n/xYdp/8pL6b/wcLd/+zs6//Ly8v/+vr6////////////5eXl/+zs6v/FxuH/LDXN/x4o3P8fKdv/Hynb/x0n2/8bJM7/GyKw/x0kqP8gJqr/ISir/yIpq/8jKqv/Iyqr/yIpq/8hJ6r/Hyaq/x0jqf8aIaj/Fh2m/xYdpv8YH6f/GB+n/xUcpv9UWbH/7+/z/9HR0f/k5OT///////r6+v/c3Nz/9fX0/2pvyP8bJdj/Hynb/x8p2/8eKNv/R0/f/5OX3f+ws+D/vL7m/8PF6P/Iyer/yszr/8zO7P/Mzuz/ycvr/8bI6f/Bw+f/u73l/7G04f+Xmtf/REm4/xcep/8YH6f/GB+n/x0jpP+vsdX/7e3s/87Ozv/8/Pz/7e3t/+bm5f/U1eb/MDjG/x4o3P8fKdv/Hijb/zQ93v/P0vf/////////////////////////////////7u75/+7u+f/////////////////////////////////Mzuz/LDOv/xcepv8YH6f/FByl/2Fltv/19fX/zMzM//Dw8P/h4eH/8vLw/52g0P8dJs//Hync/x8p2/8cJtr/XWTl//j4/v///////////////////////////+nq9/9iZsP/YWbD/+np9/////////////////////////////j4/P9YXb//FBym/xgfp/8WHaf/MDao/9zd6v/Z2dj/39/f/9zc3P/29vT/bnLD/xsl1f8fKdv/Hynb/xsl2v91e+n////////////////////////////r7Pf/ZmrF/xYdpv8WHab/ZWrE/+vs9////////////////////////////3J2yf8UG6X/GB+n/xgfp/8cI6T/t7nZ/+fn5f/S0tL/3Nzc//Hx8/9RV73/HCbY/x8p2/8fKdv/GyXa/3+E6v//////////////////////7e74/2pvxv8XHqf/GB+n/xgfp/8XHqf/am7G/+3u+P//////////////////////e3/N/xQbpv8YH6f/GB+n/xYdpP+Ymsz/8PDt/8zMzP/d3d3/7Ozw/0NKuv8cJtn/Hynb/x8p2/8bJdr/gYbq///////////////////////k5fX/naDa/y40r/8XHqb/Fx6m/y40r/+doNr/5OX1//////////////////////99gc3/FBum/xgfp/8YH6b/Fh2t/4iM0f/z8/D/ysrK/97e3f/r6+//QUi5/xwm2f8fKdv/Hynb/xsl2v+Bhur////////////////////////////q6vf/O0G0/xYdpv8WHab/O0G0/+rq9////////////////////////////32Bzf8UG6b/GB+m/xkhr/8aI83/h4vb//Pz8P/Kysr/3d3d/+/v8f9KULf/HCbX/x8p2/8fKdv/GyXa/3+F6v///////////////////////////+rq9/87QbT/Fh2m/xYdpv87QbT/6ur3////////////////////////////fIDN/xQbpf8ZIa//HSfP/xwm2f+Slt3/8fHu/83Nzf/e3t7/9fX0/2Bluf8aJNL/Hynb/x8p2/8bJdr/dnzp////////////////////////////6er3/zk/tP8TGqX/Exql/zk+tP/p6vf///////////////////////////90eMn/FR2t/x0nz/8fKdz/ICnX/6yv4v/r6+j/09PT/+Pj4//29fP/iYzD/xojx/8fKdz/Hynb/xwm2v9eZeX/+Pn+///////////////////////u7vj/YGXC/0FHtv9BR7b/YGXC/+7u+P//////////////////////+fn8/1xhyP8aI87/Hync/x4o2/8sNdT/0NHr/+Dg3v/f39//7e3t/+3t7P/Awdr/Iyu3/x4o2v8fKdv/Hijb/zM93v/P0ff///////////////////////7+///09fr/8vP5//Lz+f/09fr//v7+///////////////////////P0fX/NDzX/x4o2/8fKdv/HCbb/1BW0//v7/T/09PT/+/v7//5+fn/4+Pj/+3t8f9MUrL/GyTQ/x8p2/8fKdv/Hijb/0pS4v+coO//tLjz/7u+9P/BxPX/xsn2/8vN9//Nz/f/zdD3/8vN9//Hyfb/wsX1/7y/9P+1uPP/m6Dv/0lR4v8eKNv/Hynb/x8p2/8eJ9j/k5fc//T08f/S0tL//Pz8///////m5ub/9PTz/6KkzP8dJbj/Hyja/x8p2/8fKdv/HSfb/x0n2/8hK9v/Iy3c/yUv3P8nMNz/KDLc/ykz3f8pM93/KDLd/ycx3P8lL9z/Iy3c/yEr2/8eKNv/HSfb/x8p2/8fKdv/HSfb/z1F0//e3+//3t7d/+Tk5P////////////b29v/k5OP/7e3x/1Zbsv8ZI8n/Hync/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8eKNv/Hijb/x4o2/8eKNv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8hKtb/mp7d//X18//R0dH/+fn5/////////////////+jo6P/w8O//ysvf/zM5rf8bJdD/Hync/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/HCbZ/2dt1P/w8PX/2dnZ/+fn5///////////////////////+/v7/+Li4v/29vX/sLLS/yoxrv8bJdD/Hync/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/xwm2f9UW9L/4OHw/+fn5v/a2tr//f39////////////////////////////9vb2/+Hh4f/4+Pf/sLLS/zM5rf8ZI8n/Hyja/x8p3P8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hynb/x4o3P8eJ9b/XGLQ/93e7//t7ev/1tbW//n5+f//////////////////////////////////////9PT0/+Hh4f/39/b/y8zf/1Zbsv8dJbj/GyTR/x4o2/8fKdz/Hynb/x8p2/8fKdv/Hynb/x8p2/8fKdv/Hync/x4o3P8bJdj/LDXN/4OH0v/q6/L/6+vq/9bW1//39/f/////////////////////////////////////////////////9vb2/+Li4v/w8O//7u/y/6OlzP9NUrL/Iyu3/xojx/8aJNL/HCXX/xwm2f8cJtn/HCbY/xsk1f8dJs//MDjG/2twyP/Gx+L/9/f2/+Li4f/b29v/+fn5////////////////////////////////////////////////////////////+/v7/+jo6P/k5OT/9fXz/+7u8v/Awtr/iYzE/2Fluf9KULf/Qki5/0RKu/9RV73/bnPD/56g0f/U1eb/9vb1/+zs6//Z2dn/5+fn//39/f////////////////////////////////////////////////////////////////////////////b29v/m5ub/4+Pj/+3t7P/29vT/9fX1/+/v8v/r6+//7Ozw//Hy8//29vX/8/Pw/+bm5f/c3Nz/5eXl//j4+P/////////////////////////////////////////////////////////////////////////////////////////////////5+fn/7e3t/+Pj4//e3t7/3t7d/97e3f/d3d3/3Nzc/9zc3P/i4uL/7e3t//r6+v//////////////////////////////////////////////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
icondata = base64.b64decode(icon)
# The temp file is icon.ico
tempFile = "icon.ico"
iconfile = open(tempFile, "wb")
# Extract the icon
iconfile.write(icondata)
iconfile.close()
root.wm_iconbitmap(tempFile)
os.remove(tempFile)
# select video url
url = tk.StringVar()
url_label = ttk.Label(root, text="Video URL: ", font=("Arial", 10))
url_label.place(x=20, y=20)
url_entry = ttk.Entry(root, width=100, textvariable=url)
url_entry.place(x=100, y=20)

# button to enable or disable audio recording
audio_button = tk.BooleanVar()
audio_check = ttk.Checkbutton(root, text="Audio Only", variable=audio_button)
audio_check.place(x=100, y=110)
audio_button.set(True)

# select folder to save video
folder_path = tk.StringVar()
folder_label = ttk.Label(root, text="Folder Path: ", font=("Arial", 10))
folder_label.place(x=20, y=50)
folder_entry = ttk.Entry(root, width=100, textvariable=folder_path)
folder_entry.place(x=100, y=50)
folder_path.set(default_folder)

# select folder button
folder_button = ttk.Button(root, text="Select Folder", command=lambda: Thread(
    target=select_folder, name="selectFolderThread").start())
folder_button.place(x=20, y=80)

# download button
download_button = ttk.Button(root, text="Download", command=lambda: Thread(
    target=download, args=(event,), name="downloadThread").start())
download_button.place(x=20, y=110)

# stop button
stop_button = ttk.Button(root, text="Stop", command=lambda: Thread(
    target=stop, args=(event,), name="stopThread").start())
stop_button.place(x=20, y=140)

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
