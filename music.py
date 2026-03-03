import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import vlc
import os
import time
import sqlite3

# ================= DATABASE =================
conn = sqlite3.connect("music.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT NOT NULL
)
""")

conn.commit()


# VLC SETUP
instance = vlc.Instance()
player = instance.media_player_new()

playlist = []
current_index = None
is_paused = False
repeat = False

# FUNCTIONS

def import_folder():
    folder = filedialog.askdirectory()
    if folder:
        for file in os.listdir(folder):
            if file.endswith(('.mp3', '.wav', '.flac')):
                path = os.path.join(folder, file)
                playlist.append(path)
                listbox.insert(tk.END, file)

def add_song():
    file = filedialog.askopenfilename(
        filetypes=[("Audio Files", "*.mp3 *.wav *.flac")]
    )
    if file:
        playlist.append(file)
        listbox.insert(tk.END, os.path.basename(file))
    
    cursor.execute("INSERT INTO songs (path) VALUES (?)", (file,))
    conn.commit()
        

def play_song(index):
    global current_index, is_paused
    current_index = index
    media = instance.media_new(playlist[index])
    player.set_media(media)
    player.play()
    is_paused = False

def toggle_play():
    global is_paused

    if player.is_playing():
        player.pause()
        is_paused = True
        return

    selected = listbox.curselection()

    if selected:
        play_song(selected[0])
    elif is_paused:
        player.play()
        is_paused = False
    elif current_index is not None:
        player.play()
    else:
        messagebox.showwarning("No song", "Select a song first")

def next_song():
    global current_index
    if current_index is None:
        return

    next_index = (current_index + 1) % len(playlist)
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(next_index)
    play_song(next_index)

def previous_song():
    global current_index
    if current_index is None:
        return

    prev_index = (current_index - 1) % len(playlist)
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(prev_index)
    play_song(prev_index)

def toggle_repeat():
    global repeat
    repeat = not repeat
    status = "ON" if repeat else "OFF"
    messagebox.showinfo("Repeat", f"Repeat is {status}")

def update_progress():
    length = player.get_length()
    current = player.get_time()

    if length > 0:
        progress.config(to=length)
        progress.set(current)

        total_time = time.strftime('%M:%S', time.gmtime(length / 1000))
        current_time = time.strftime('%M:%S', time.gmtime(current / 1000))
        time_label.config(text=f"{current_time} / {total_time}")

        # Auto next or repeat
        if player.get_state() == vlc.State.Ended:
            if repeat:
                player.play()
            else:
                next_song()

    root.after(1000, update_progress)

def seek_song(value):
    if player.get_length() > 0:
        player.set_time(int(float(value)))

def set_volume(value):
    player.audio_set_volume(int(float(value)))
    
def load_from_database():
    cursor.execute("SELECT path FROM songs")
    rows = cursor.fetchall()

    for row in rows:
        song_path = row[0]
        if os.path.exists(song_path):
            playlist.append(song_path)
            listbox.insert(tk.END, os.path.basename(song_path))

# UI

root = tk.Tk()
root.title("NK Music Player")
root.geometry("750x550")

listbox = tk.Listbox(root, width=85, height=15)
listbox.pack(pady=10)

control_frame = tk.Frame(root)
control_frame.pack(pady=10)

tk.Button(control_frame, text="Import Folder", command=import_folder).grid(row=0, column=0, padx=5)
tk.Button(control_frame, text="Add Song", command=add_song).grid(row=0, column=1, padx=5)
tk.Button(control_frame, text="Previous", command=previous_song).grid(row=0, column=2, padx=5)
tk.Button(control_frame, text="Play/Pause", command=toggle_play).grid(row=0, column=3, padx=5)
tk.Button(control_frame, text="Next", command=next_song).grid(row=0, column=4, padx=5)
tk.Button(control_frame, text="Repeat", command=toggle_repeat).grid(row=0, column=5, padx=5)

progress = ttk.Scale(root, from_=0, to=100, orient="horizontal", length=600, command=seek_song)
progress.pack(pady=10)

time_label = tk.Label(root, text="00:00 / 00:00")
time_label.pack()

tk.Label(root, text="Volume").pack()
volume_slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", command=set_volume)
volume_slider.set(70)
player.audio_set_volume(70)
volume_slider.pack(pady=5)

update_progress()
load_from_database()
root.mainloop()
