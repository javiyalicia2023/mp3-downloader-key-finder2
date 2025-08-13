import os
import shutil

from tkinter import (
    filedialog,
    messagebox,
    Listbox,
    Frame,
    Text,
    Label,
    Button,
    Entry,
    StringVar,
    END,
    BOTH,
    LEFT,
    X,
    NW,
)
from tkinter import ttk

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES

    BaseTk = TkinterDnD.Tk
    DND_AVAILABLE = True
except Exception:  # pragma: no cover - tkinterdnd2 optional
    from tkinter import Tk as BaseTk

    DND_AVAILABLE = False

from youtube_audio import download_audio
from key_finder import estimate_key
from audio_features import analyze_features, describe_score


class App:
    """Graphical interface for downloading and analyzing audio."""

    def __init__(self) -> None:
        self.root = BaseTk()
        self.root.title("MP3 Downloader & Analyzer")
        self.root.configure(bg="black")

        self.download_dir = StringVar(value="downloads")

        # Directory selector
        dir_frame = Frame(self.root, bg="black")
        dir_frame.pack(padx=10, pady=10, fill=X)
        Label(
            dir_frame, text="Download directory:", fg="white", bg="black"
        ).pack(side=LEFT)
        Entry(dir_frame, textvariable=self.download_dir, width=40).pack(
            side=LEFT, padx=5
        )
        Button(
            dir_frame,
            text="Browse",
            command=self.choose_dir,
            bg="#2F5BF9",
            fg="white",
        ).pack(side=LEFT)

        # URL downloader
        url_frame = Frame(self.root, bg="black")
        url_frame.pack(padx=10, pady=10, fill=X)
        Label(url_frame, text="YouTube URL:", fg="white", bg="black").pack(side=LEFT)
        self.url_var = StringVar()
        Entry(url_frame, textvariable=self.url_var, width=40).pack(side=LEFT, padx=5)
        self.bitrate_var = StringVar(value="160")
        ttk.OptionMenu(url_frame, self.bitrate_var, "160", "160", "320").pack(
            side=LEFT, padx=5
        )
        Button(
            url_frame,
            text="Download",
            command=self.download_url,
            bg="#2F5BF9",
            fg="white",
        ).pack(side=LEFT)

        # File list
        list_frame = Frame(self.root, bg="black")
        list_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)
        Label(list_frame, text="Files:", fg="white", bg="black").pack(anchor=NW)
        self.listbox = Listbox(list_frame, bg="black", fg="white")
        self.listbox.pack(fill=BOTH, expand=True)
        Button(
            list_frame,
            text="Analyze Selected",
            command=self.analyze_selected,
            bg="#2F5BF9",
            fg="white",
        ).pack(pady=5)

        # Import button
        Button(
            self.root,
            text="Import and Analyze File",
            command=self.import_file,
            bg="#2F5BF9",
            fg="white",
        ).pack(pady=5)

        # Drag-and-drop area
        if DND_AVAILABLE:
            drop_label = Label(
                self.root,
                text="Drop audio file here",
                fg="white",
                bg="#2F5BF9",
                relief="ridge",
                width=40,
                height=3,
            )
            drop_label.pack(padx=10, pady=10, fill=X)
            drop_label.drop_target_register(DND_FILES)
            drop_label.dnd_bind("<<Drop>>", self.drop_file)

        # Results display
        self.result_text = Text(self.root, height=8, bg="black", fg="white")
        self.result_text.pack(fill=BOTH, padx=10, pady=10)

        self.refresh_file_list()
        self.root.mainloop()

    def choose_dir(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.download_dir.set(path)
            self.refresh_file_list()

    def refresh_file_list(self) -> None:
        self.listbox.delete(0, END)
        directory = self.download_dir.get()
        if os.path.isdir(directory):
            for name in sorted(os.listdir(directory)):
                if name.lower().endswith(".mp3"):
                    self.listbox.insert(END, name)

    def download_url(self) -> None:
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        try:
            bitrate = int(self.bitrate_var.get())
            path = download_audio(
                url, bitrate=bitrate, output_dir=self.download_dir.get()
            )
            self.refresh_file_list()
            self.display_features(path)
        except Exception as exc:  # pragma: no cover - depends on network
            messagebox.showerror("Download error", str(exc))

    def analyze_selected(self) -> None:
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Select a file to analyze.")
            return
        filename = self.listbox.get(selection[0])
        path = os.path.join(self.download_dir.get(), filename)
        self.display_features(path)

    def import_file(self) -> None:
        filepath = filedialog.askopenfilename(
            filetypes=[("Audio files", "*.mp3 *.wav *.ogg *.flac")]
        )
        if filepath:
            dest = os.path.join(self.download_dir.get(), os.path.basename(filepath))
            shutil.copy(filepath, dest)
            self.refresh_file_list()
            self.display_features(dest)

    def drop_file(self, event) -> None:  # pragma: no cover - GUI interaction
        filepath = event.data.strip()
        if filepath.startswith("{") and filepath.endswith("}"):
            filepath = filepath[1:-1]
        if os.path.isfile(filepath):
            dest = os.path.join(self.download_dir.get(), os.path.basename(filepath))
            shutil.copy(filepath, dest)
            self.refresh_file_list()
            self.display_features(dest)

    def display_features(self, path: str) -> None:
        key, alt_key = estimate_key(path)
        feats = analyze_features(path)
        lines = [
            f"File: {os.path.basename(path)}",
            f"Key: {key} (Relative: {alt_key})",
            f"BPM: {feats['bpm']:.2f}",
            f"Energy: {feats['energy']:.2f} ({describe_score(feats['energy'])})",
            f"Danceability: {feats['danceability']:.2f} ({describe_score(feats['danceability'])})",
            f"Happiness: {feats['happiness']:.2f} ({describe_score(feats['happiness'])})",
            "",
        ]
        self.result_text.delete(1.0, END)
        self.result_text.insert(END, "\n".join(lines))


if __name__ == "__main__":  # pragma: no cover - manual launch
    App()

