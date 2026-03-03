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
current_index = None

#Functions
def add_song():
    files = filedialog.askopenfilenames(
        filetypes=[("Audio Files","*.mp3 *.wav")]
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
    
if player.get_state() == vlc.State.Ended:
    player.play()
# def callback_function():
#     player.stop()
#     player.play()
    

# events = player.event_manager()
# events.event_attach(vlc.EventType.MediaPlayerEndReached, callback_function)

     
def next_song():
    if current_index is None:
        return

    next_index = current_index + 1

    if next_index < playlist.size():
        playlist.selection_clear(0, tk.END)
        playlist.selection_set(next_index)
        playlist.activate(next_index)
        current_index = next_index
        play_song()
        
def previous_song():
    selected = playlist.curselection()

    if not selected:
        return

    current_index = selected[0]
    prev_index = current_index - 1
    
    if prev_index >= 0:
        playlist.selection_clear(0, tk.END)
        playlist.selection_set(prev_index)
        playlist.activate(prev_index)
        current_index = prev_index
        play_song()
    
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
# tk.Button(btn_frame, text="Repeat", command=callback_function).grid(row=0, column=3, padx=5)
tk.Button(btn_frame, text="Previous", command=previous_song).grid(row=0, column=4, padx=5)
tk.Button(btn_frame, text="Next", command=next_song).grid(row=0, column=5, padx=5)

# progress = tk.Scale(
# root,
# from_=0,
# to=100,
# orient="horizontal",
# length=500,
# command=seek_song
# )

volume_slider = tk.Scale(
root,
from_=0,
to=100,
orient="horizontal",
label="Volume",
command=set_volume
)
volume_slider.set(70)
volume_slider.pack(fill="x", padx=10)
root.mainloop()
