import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import vlc
import os
import time
import threading


root = tk.Tk()
root.title("Music Player")
root.geometry("700x500")

# VLC Player
instance = vlc.Instance()
player = instance.media_player_new()

playlist = []
current_index = None
is_paused = False
repeat = False



# FUNCTIONS
# IMPORT
def import_folder():
    folder = filedialog.askdirectory()
    if folder:
        for file in os.listdir(folder):
            if file.endswith(('.mp3', '.wav', '.flac')):
                full_path = os.path.join(folder, file)
                playlist.append(full_path)
                listbox.insert(tk.END, file)

def add_song():
    file = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav *.flac")])
    if file:
        playlist.append(file)
        listbox.insert(tk.END, os.path.basename(file))

# PLAY
def play_song():
    selected = listbox.curselection()

    # If user selected a song from list
    if selected:
        current_index = selected[0]

        media = instance.media_new(playlist[current_index])
        player.set_media(media)
        player.play()
        is_paused = False
        return

    # If no selection but song was paused → resume
    if is_paused:
        player.play()
        is_paused = False
        return

    # If nothing selected and nothing paused
    if current_index is None:
        messagebox.showwarning("No song", "Select a song first")
# def play_song():
#     selected = listbox.curselection()
#     if selected:
#         current_index = selected[0]
#     if current_index is None:
#             messagebox.showwarning("No song", "Select a song first")
#             return
    
#     media = instance.media_new(playlist[current_index])
#     player.set_media(media)
#     player.play()
#     is_paused = False
    
#     # If paused and same song → resume
#     if is_paused and new_index == current_index:
#         player.play()
#         is_paused = False
#         return

    # Otherwise start new song
    current_index = new_index
    media = instance.media_new(playlist[current_index])
    player.set_media(media)
    player.play()
    is_paused = False

# PAUSE
def pause_song():
    if player.is_playing():
        player.pause()
        is_paused = True

# REPEAT 
def toggle_repeat():
    repeat = not repeat
    if repeat:
        messagebox.showinfo("Repeat", "Repeat is ON")
    else:
        messagebox.showinfo("Repeat", "Repeat is OFF")

# PROGRESS
def update_progress():
    if player is not None:
        length = player.get_length()
        current = player.get_time()

    if length > 0:
        progress["maximum"] = length
        progress["value"] = current

    total_time = time.strftime('%M:%S', time.gmtime(length/1000))
    current_time = time.strftime('%M:%S', time.gmtime(current/1000))

    time_label.config(text=f"{current_time} / {total_time}")

# Repeat logic
# if current >= length - 1000 and length > 0:
#     if repeat:
#         player.stop()
#         play_song()

# root.after(1000, update_progress)

# Playlist box
listbox = tk.Listbox(root, width=80, height=15)
listbox.pack(pady=10)

# Buttons frame
frame = tk.Frame(root)
frame.pack()

tk.Button(frame, text="Import Folder", command=import_folder).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Add Song", command=add_song).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Play", command=play_song).grid(row=0, column=2, padx=5)
tk.Button(frame, text="Pause", command=pause_song).grid(row=0, column=3, padx=5)
tk.Button(frame, text="Repeat", command=toggle_repeat).grid(row=0, column=4, padx=5)

# Progress bar
progress = ttk.Progressbar(root, orient="horizontal", length=600, mode="determinate")
progress.pack(pady=10)

time_label = tk.Label(root, text="00:00 / 00:00")
time_label.pack()


root.mainloop()