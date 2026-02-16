import tkinter as tk
from tkinter import filedialog,messagebox
import vlc
import os



root = tk.Tk()
root.title("Music Player")
root.geometry("650x300")

# VLC Player
instance = vlc.Instance()
player = instance.media_player_new()

current_song = None

#Functions
def add_song():
    files = fieldialog.askopenfilenames(
        Filetypes=[("Audio","*.mp3","*.wav")]
    )
    for file in files:
        playlist.insert(tk.END, file)
        
def play_song():
    try:
        selected = playlist.get(tk.ACTIVE)
        if not selected:
            messagebox.showwarning("Select a song first!")
            return
        media = instance.media_new(selected)
        player.set_media(media)
        player.play()

    except Exception as e:
            messagebox.showerror("Error", str(e))
            
def pause_song():
    player.pause()
    
def repeat_song():
    player.repeat()
    
def set_volume(value):
    player.audio_set_volume(int(value))
# Playlist (Listbox)
playlist = tk.Listbox(root, font=("Arial", 11))
playlist.pack(fill="both", expand=True, padx=10, pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Add Song", command=add_song).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Play", command=play_song).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Pause", command=pause_song).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Repeat", command=repeat_song).grid(row=0, column=3, padx=5)

root = tk.Tk()
root.mainloop()