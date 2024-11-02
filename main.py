import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import subprocess
import os

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Downloader")
        self.root.geometry("380x380")  # Width and height
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # URL Entry
        self.url_label = tk.Label(root, text="YouTube URL:", bg="#f0f0f0", font=("Helvetica", 12))
        self.url_label.pack(pady=5)
        self.url_entry = tk.Entry(root, width=55)
        self.url_entry.pack(pady=5)
        self.url_entry.bind("<Return>", self.download_audio)  # Bind Enter key

        # Download Directory Selection
        self.download_dir_label = tk.Label(root, text="Download Directory:", bg="#f0f0f0", font=("Helvetica", 12))
        self.download_dir_label.pack(pady=5)

        self.download_dir_var = tk.StringVar(value="Select Directory")
        self.download_dir_entry = tk.Entry(root, textvariable=self.download_dir_var, state='readonly', width=50)
        self.download_dir_entry.pack(pady=5)

        self.browse_button = tk.Button(
            root,
            text="Browse",
            command=self.browse_directory,
            bg="#A0C4FF",  # Light blue-gray color
            fg="black",
            font=("Helvetica", 12),
            padx=10,
            pady=5
        )
        self.browse_button.pack(pady=5)

        # Frame for Audio Quality and Format Selection
        self.audio_frame = tk.Frame(root, bg="#f0f0f0")
        self.audio_frame.pack(pady=10)

        # Audio Quality Selection
        self.audio_quality_label = tk.Label(self.audio_frame, text="Quality:", bg="#f0f0f0", font=("Helvetica", 12))
        self.audio_quality_label.grid(row=0, column=0, padx=5, pady=5)

        self.audio_quality_var = tk.StringVar(value="192kbps")  # Default value
        self.audio_quality_combobox = ttk.Combobox(self.audio_frame, textvariable=self.audio_quality_var)
        self.audio_quality_combobox['values'] = ["128kbps", "192kbps", "256kbps", "320kbps"]
        self.audio_quality_combobox.grid(row=1, column=0, padx=5, pady=5)

        # Format Selection
        self.format_label = tk.Label(self.audio_frame, text="Format:", bg="#f0f0f0", font=("Helvetica", 12))
        self.format_label.grid(row=0, column=1, padx=5, pady=5)

        self.format_var = tk.StringVar(value="mp3")  # Default value
        self.format_combobox = ttk.Combobox(self.audio_frame, textvariable=self.format_var)
        self.format_combobox['values'] = ["mp3", "wav", "flac"]
        self.format_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Download Button
        self.download_button = tk.Button(root, text="Download", command=self.download_audio, bg="#007bff", fg="white", font=("Helvetica", 14))
        self.download_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(root, text="", bg="#f0f0f0", font=("Helvetica", 10))
        self.status_label.pack(pady=5)

        self.success_label = tk.Label(root, text="", bg="#f0f0f0", font=("Helvetica", 10), fg="green")
        self.success_label.pack(pady=5)

    def browse_directory(self):
        directory = filedialog.askdirectory()  # Opens a dialog to select directory
        if directory:  # If a directory is selected
            self.download_dir_var.set(directory)

    def download_audio(self, event=None):
        video_url = self.url_entry.get()
        download_dir = self.download_dir_var.get()
        selected_quality = self.audio_quality_var.get()
        selected_format = self.format_var.get()

        if not video_url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return

        if download_dir == "Select Directory":
            messagebox.showerror("Error", "Please select a download directory.")
            return
        
        # Check if the directory exists
        if not os.path.exists(download_dir):
            messagebox.showerror("Error", "The selected directory does not exist.")
            return

        # Prepare the command
        quality_kbps = selected_quality[:-3]  # Remove 'kbps' for command
        command = [
            'yt-dlp',
            '-o', f'{download_dir}/%(title)s.%(ext)s',  # Output template
            '-f', f'bestaudio[abr<={quality_kbps}]',
            '--extract-audio',
            '--audio-format', selected_format,
            video_url
        ]

        try:
            self.status_label.config(text="Downloading...")
            self.root.update()  # Update the status label immediately
            subprocess.run(command, check=True)
            self.success_label.config(text=f"Downloaded successfully to {download_dir}")
            self.status_label.config(text="")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.success_label.config(text="")  # Clear success message

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
