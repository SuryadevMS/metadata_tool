from moviepy.editor import VideoFileClip
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class VideoMetadataTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Metadata Tool")
        self.root.geometry("1000x720")
        
        self.selected_file = None

        self.file_label = tk.Label(root, text="Selected File:")
        self.file_label.pack(pady=10)

        self.file_entry = tk.Entry(root, width=50, state="disabled")
        self.file_entry.pack(pady=5)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=5)

        self.extract_button = tk.Button(root, text="Extract Metadata", command=self.extract_metadata)
        self.extract_button.pack(pady=5)

        self.export_button = tk.Button(root, text="Export Metadata", command=self.export_metadata)
        self.export_button.pack(pady=5)

        self.metadata_display = tk.Text(root, height=20, width=80)
        self.metadata_display.pack(pady=10)

    def browse_file(self):
        filetypes = (("Video files", "*.mp4;*.mkv"), ("All files", "*.*"))
        file_path = filedialog.askopenfilename(title="Select Video File", filetypes=filetypes)
        if file_path:
            self.selected_file = file_path
            self.file_entry.config(state="normal")
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.file_entry.config(state="disabled")

    def extract_metadata(self):
        if self.selected_file:
            try:
                video = VideoFileClip(self.selected_file)
                duration = video.duration
                metadata = video.reader.infos
                filename = os.path.basename(self.selected_file)
                video.close()
                metadata_str = f"Filename: {filename}\nDuration: {int(duration/60)} minutes, {int(duration%60)} seconds\n"
                for key, value in metadata.items():
                    if key != "duration":
                        metadata_str += f"{key}: {value}\n"
                self.metadata_display.config(state='normal')
                self.metadata_display.delete("1.0", tk.END)
                self.metadata_display.insert(tk.END, metadata_str)
                self.metadata_display.config(state='disabled')
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showwarning("Video Metadata", "Please select a video file.")

    def export_metadata(self):
        if self.selected_file:
            try:
                video = VideoFileClip(self.selected_file)
                duration = video.duration
                metadata = video.reader.infos
                filename = os.path.basename(self.selected_file)
                video.close()
                save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")], title="Save Metadata")
                if save_path:
                    with open(save_path, 'w') as f:
                        f.write(f"Filename: {filename}\nDuration: {int(duration/60)} minutes, {int(duration%60)} seconds\n")
                        for key, value in metadata.items():
                            if key != "duration":
                                f.write(f"{key}: {value}\n")
                    messagebox.showinfo("Export Metadata", "Metadata exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        else:
            messagebox.showwarning("Export Metadata", "Please select a video file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoMetadataTool(root)
    root.mainloop()
