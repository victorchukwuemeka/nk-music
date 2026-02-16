# import vlc

# player = vlc.MediaPlayer("your_song.mp3")
# player.play()

# input("Press Enter to stop...")
# player.stop()

import tkinter as tk
from tkinter import filedialog, messagebox
import vlc
import os

# If VLC DLL error happens, uncomment and adjust path:
# os.add_dll_directory(r"C:\Program Files\VideoLAN\VLC")

class MusicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VLC Music Player")
        self.root.geometry("500x450")

        # VLC Player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.current_song = None

        # Playlist (Listbox)
        self.playlist = tk.Listbox(root, font=("Arial", 11))
        self.playlist.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Add Song", command=self.add_song).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Play", command=self.play_song).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Pause", command=self.pause_song).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Stop", command=self.stop_song).grid(row=0, column=3, padx=5)

        # Volume Slider
        self.volume_slider = tk.Scale(
            root,
            from_=0,
            to=100,
            orient="horizontal",
            label="Volume",
            command=self.set_volume
        )
        self.volume_slider.set(70)
        self.volume_slider.pack(fill="x", padx=10)

    # ---------------- FUNCTIONS ---------------- #

    def add_song(self):
        files = filedialog.askopenfilenames(
            filetypes=[("Audio Files", "*.mp3 *.wav")]
        )
        for file in files:
            self.playlist.insert(tk.END, file)

    def play_song(self):
        try:
            selected = self.playlist.get(tk.ACTIVE)
            if not selected:
                messagebox.showwarning("Warning", "Select a song first!")
                return

            media = self.instance.media_new(selected)
            self.player.set_media(media)
            self.player.play()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def pause_song(self):
        self.player.pause()

    def stop_song(self):
        self.player.stop()

    def set_volume(self, value):
        self.player.audio_set_volume(int(value))


# Run the app
root = tk.Tk()
app = MusicApp(root)
root.mainloop()