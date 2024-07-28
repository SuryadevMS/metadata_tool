import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ExifTags

class ImageMetadataTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Metadata Tool")
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

        self.remove_button = tk.Button(root, text="Remove Metadata", command=self.remove_metadata)
        self.remove_button.pack(pady=5)

        self.export_button = tk.Button(root, text="Export Metadata", command=self.export_metadata)
        self.export_button.pack(pady=5)

        self.metadata_display = tk.Text(root, height=20, width=80)
        self.metadata_display.pack(pady=10)

    def browse_file(self):
        filetypes = (("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*"))
        file_path = filedialog.askopenfilename(title="Select Image File", filetypes=filetypes)
        if file_path:
            self.selected_file = file_path
            self.file_entry.config(state="normal")
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
            self.file_entry.config(state="disabled")

    def extract_metadata(self):
        if self.selected_file:
            image = Image.open(self.selected_file)
            exif_data = image._getexif()
            if exif_data:
                metadata_str = ""
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    metadata_str += f"{tag_name}: {value}\n"
                self.metadata_display.config(state='normal')
                self.metadata_display.delete("1.0", tk.END)
                self.metadata_display.insert(tk.END, metadata_str)
                self.metadata_display.config(state='disabled')
            else:
                messagebox.showinfo("Image Metadata", "No metadata found for selected image.")
            image.close()
        else:
            messagebox.showwarning("Image Metadata", "Please select an image file.")

    def remove_metadata(self):
        if self.selected_file:
            image = Image.open(self.selected_file)
            save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")], title="Save Image Without Metadata")
            if save_path:
                image.save(save_path)
                messagebox.showinfo("Remove Metadata", "Metadata removed and image saved successfully.")
            image.close()
        else:
            messagebox.showwarning("Remove Metadata", "Please select an image file.")

    def export_metadata(self):
        if self.selected_file:
            image = Image.open(self.selected_file)
            exif_data = image._getexif()
            if exif_data:
                save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")], title="Save Metadata")
                if save_path:
                    with open(save_path, 'w') as f:
                        for tag, value in exif_data.items():
                            tag_name = ExifTags.TAGS.get(tag, tag)
                            f.write(f"{tag_name}: {value}\n")
                    messagebox.showinfo("Export Metadata", "Metadata exported successfully.")
            else:
                messagebox.showinfo("Export Metadata", "No metadata found for selected image.")
            image.close()
        else:
            messagebox.showwarning("Export Metadata", "Please select an image file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageMetadataTool(root)
    root.mainloop()
