import os
import shutil
import sys

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
from i18n import set_language, t


class App:
    """Graphical interface for downloading and analyzing audio."""

    def __init__(self, lang: str = "en") -> None:
        set_language(lang)
        self.root = BaseTk()
        self.root.title(t("app_title"))
        self.root.configure(bg="black")

        self.download_dir = StringVar(value="downloads")

        # Directory selector
        dir_frame = Frame(self.root, bg="black")
        dir_frame.pack(padx=10, pady=10, fill=X)
        Label(
            dir_frame, text=t("download_directory"), fg="white", bg="black"
        ).pack(side=LEFT)
        Entry(dir_frame, textvariable=self.download_dir, width=40).pack(
            side=LEFT, padx=5
        )
        Button(
            dir_frame,
            text=t("browse"),
            command=self.choose_dir,
            bg="#2F5BF9",
            fg="white",
        ).pack(side=LEFT)

        # URL downloader
        url_frame = Frame(self.root, bg="black")
        url_frame.pack(padx=10, pady=10, fill=X)
        Label(url_frame, text=t("youtube_url"), fg="white", bg="black").pack(side=LEFT)
        self.url_var = StringVar()
        Entry(url_frame, textvariable=self.url_var, width=40).pack(side=LEFT, padx=5)
        self.bitrate_var = StringVar(value="160")
        ttk.OptionMenu(url_frame, self.bitrate_var, "160", "160", "320").pack(
            side=LEFT, padx=5
        )
        Button(
            url_frame,
            text=t("download"),
            command=self.download_url,
            bg="#2F5BF9",
            fg="white",
        ).pack(side=LEFT)

        # File list
        list_frame = Frame(self.root, bg="black")
        list_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)
        Label(list_frame, text=t("files"), fg="white", bg="black").pack(anchor=NW)
        self.listbox = Listbox(list_frame, bg="black", fg="white")
        self.listbox.pack(fill=BOTH, expand=True)
        Button(
            list_frame,
            text=t("analyze_selected"),
            command=self.analyze_selected,
            bg="#2F5BF9",
            fg="white",
        ).pack(pady=5)

        # Import button
        Button(
            self.root,
            text=t("import_analyze"),
            command=self.import_file,
            bg="#2F5BF9",
            fg="white",
        ).pack(pady=5)

        # Drag-and-drop area
        if DND_AVAILABLE:
            drop_label = Label(
                self.root,
                text=t("drop_audio"),
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
            messagebox.showerror(t("error"), t("enter_url"))
            return
        try:
            bitrate = int(self.bitrate_var.get())
            path = download_audio(
                url, bitrate=bitrate, output_dir=self.download_dir.get()
            )
            self.refresh_file_list()
            self.display_features(path)
        except Exception as exc:  # pragma: no cover - depends on network
            messagebox.showerror(t("download_error"), str(exc))

    def analyze_selected(self) -> None:
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo(t("info"), t("select_file"))
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
            f"{t('file')}: {os.path.basename(path)}",
            f"{t('detected_key')}: {key} ({t('relative_key')}: {alt_key})",
            f"{t('bpm')}: {feats['bpm']:.2f}",
            f"{t('energy')}: {feats['energy']:.2f} ({describe_score(feats['energy'])})",
            f"{t('danceability')}: {feats['danceability']:.2f} ({describe_score(feats['danceability'])})",
            f"{t('happiness')}: {feats['happiness']:.2f} ({describe_score(feats['happiness'])})",
            "",
        ]
        self.result_text.delete(1.0, END)
        self.result_text.insert(END, "\n".join(lines))


if __name__ == "__main__":  # pragma: no cover - manual launch
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    App(lang)

