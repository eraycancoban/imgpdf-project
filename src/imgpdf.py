import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import datetime

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image to PDF Merger")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.minsize(800, 500)
        
        self.selected_files = []
        self.rotation_info = {}
        self.output_pdf = ""
        self.preview_image = None
        
        self.create_widgets()
        
    def create_widgets(self):
        title_label = tk.Label(self.root, text="Image to PDF Merger", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        left_frame = tk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)
        
        select_btn = tk.Button(left_frame, text="Select Image Files", command=self.select_files,
                              font=("Arial", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
        select_btn.grid(row=0, column=0, pady=10, sticky="ew")
        
        self.files_frame = tk.Frame(left_frame)
        self.files_frame.grid(row=2, column=0, sticky="nsew")
        
        self.files_frame.columnconfigure(0, weight=1)
        self.files_frame.rowconfigure(0, weight=1)
        
        scrollbar = tk.Scrollbar(self.files_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        self.files_listbox = tk.Listbox(self.files_frame, selectmode=tk.EXTENDED, 
                                       font=("Arial", 10))
        self.files_listbox.grid(row=0, column=0, sticky="nsew")
        
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.files_listbox.yview)
        
        self.files_listbox.bind("<<ListboxSelect>>", lambda event: self.preview_selected_image())
        
        btn_frame = tk.Frame(left_frame)
        btn_frame.grid(row=3, column=0, sticky="ew", pady=5)
        
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        btn_frame.columnconfigure(2, weight=1)
        
        remove_btn = tk.Button(btn_frame, text="Remove Selected", command=self.remove_selected,
                              font=("Arial", 10), bg="#f44336", fg="white")
        remove_btn.grid(row=0, column=0, padx=2, sticky="ew")
        
        up_btn = tk.Button(btn_frame, text="Move Up", command=self.move_up,
                         font=("Arial", 10))
        up_btn.grid(row=0, column=1, padx=2, sticky="ew")
        
        down_btn = tk.Button(btn_frame, text="Move Down", command=self.move_down,
                           font=("Arial", 10))
        down_btn.grid(row=0, column=2, padx=2, sticky="ew")
        
        orientation_frame = tk.Frame(left_frame)
        orientation_frame.grid(row=4, column=0, sticky="ew", pady=5)
        
        orientation_frame.columnconfigure(0, weight=1)
        orientation_frame.columnconfigure(1, weight=1)
        
        portrait_btn = tk.Button(orientation_frame, text="All Portrait", 
                               command=lambda: self.set_orientation("portrait"),
                               font=("Arial", 10), bg="#607D8B", fg="white")
        portrait_btn.grid(row=0, column=0, padx=2, sticky="ew")
        
        landscape_btn = tk.Button(orientation_frame, text="All Landscape", 
                                command=lambda: self.set_orientation("landscape"),
                                font=("Arial", 10), bg="#607D8B", fg="white")
        landscape_btn.grid(row=0, column=1, padx=2, sticky="ew")
        
        create_btn = tk.Button(left_frame, text="Create PDF", command=self.create_pdf,
                              font=("Arial", 12), bg="#2196F3", fg="white", padx=20, pady=5)
        create_btn.grid(row=5, column=0, pady=10, sticky="ew")
        
        right_frame = tk.Frame(main_frame, bg="#f5f5f5", relief=tk.GROOVE, borderwidth=2)
        right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        preview_title = tk.Label(right_frame, text="Image Preview", font=("Arial", 12, "bold"), bg="#f5f5f5")
        preview_title.grid(row=0, column=0, pady=5)
        
        self.preview_frame = tk.Frame(right_frame, bg="#f5f5f5")
        self.preview_frame.grid(row=1, column=0, sticky="nsew", pady=10, padx=10)
        
        self.preview_frame.columnconfigure(0, weight=1)
        self.preview_frame.rowconfigure(0, weight=1)
        
        self.preview_label = tk.Label(self.preview_frame, bg="#f5f5f5", text="No image selected")
        self.preview_label.grid(row=0, column=0, sticky="nsew")
        
        rotation_frame = tk.Frame(right_frame, bg="#f5f5f5")
        rotation_frame.grid(row=2, column=0, sticky="ew", pady=5)
        
        rotation_frame.columnconfigure(0, weight=1)
        rotation_frame.columnconfigure(1, weight=1)
        rotation_frame.columnconfigure(2, weight=1)
        
        rotate_left_btn = tk.Button(rotation_frame, text="Rotate Left", command=lambda: self.rotate_image(-90),
                                  font=("Arial", 10), bg="#FF9800", fg="white")
        rotate_left_btn.grid(row=0, column=0, padx=2, sticky="ew")
        
        rotate_right_btn = tk.Button(rotation_frame, text="Rotate Right", command=lambda: self.rotate_image(90),
                                   font=("Arial", 10), bg="#FF9800", fg="white")
        rotate_right_btn.grid(row=0, column=1, padx=2, sticky="ew")
        
        rotate_180_btn = tk.Button(rotation_frame, text="Rotate 180°", command=lambda: self.rotate_image(180),
                                 font=("Arial", 10), bg="#FF9800", fg="white")
        rotate_180_btn.grid(row=0, column=2, padx=2, sticky="ew")
        
        self.info_label = tk.Label(right_frame, text="", bg="#f5f5f5", font=("Arial", 9))
        self.info_label.grid(row=3, column=0, pady=5)
        
        self.root.bind('<Configure>', self.on_window_resize)
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
        )
        
        if files:
            for file in files:
                if file not in self.selected_files:
                    self.selected_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
                    self.rotation_info[file] = 0
                    
            if len(self.selected_files) == len(files):
                self.files_listbox.selection_set(0)
                self.preview_selected_image()
    
    def remove_selected(self):
        selected_indices = self.files_listbox.curselection()
        
        for i in sorted(selected_indices, reverse=True):
            file_path = self.selected_files[i]
            self.files_listbox.delete(i)
            self.selected_files.pop(i)
            if file_path in self.rotation_info:
                del self.rotation_info[file_path]
                
        self.preview_selected_image()
    
    def move_up(self):
        selected_indices = self.files_listbox.curselection()
        
        if not selected_indices or selected_indices[0] == 0:
            return
            
        for index in selected_indices:
            if index > 0:
                self.selected_files[index], self.selected_files[index-1] = \
                    self.selected_files[index-1], self.selected_files[index]
                
                text = self.files_listbox.get(index)
                self.files_listbox.delete(index)
                self.files_listbox.insert(index-1, text)
                self.files_listbox.selection_set(index-1)
    
    def move_down(self):
        selected_indices = self.files_listbox.curselection()
        
        if not selected_indices or selected_indices[-1] == self.files_listbox.size()-1:
            return
            
        for index in sorted(selected_indices, reverse=True):
            if index < self.files_listbox.size()-1:
                self.selected_files[index], self.selected_files[index+1] = \
                    self.selected_files[index+1], self.selected_files[index]
                
                text = self.files_listbox.get(index)
                self.files_listbox.delete(index)
                self.files_listbox.insert(index+1, text)
                self.files_listbox.selection_set(index+1)
    
    def rotate_image(self, degrees):
        selected_indices = self.files_listbox.curselection()
        
        if not selected_indices:
            messagebox.showinfo("Info", "Please select an image to rotate")
            return
            
        for index in selected_indices:
            file_path = self.selected_files[index]
            current_rotation = self.rotation_info.get(file_path, 0)
            new_rotation = (current_rotation + degrees) % 360
            self.rotation_info[file_path] = new_rotation
            
            filename = os.path.basename(file_path)
            if new_rotation != 0:
                self.files_listbox.delete(index)
                self.files_listbox.insert(index, f"{filename} (Rotated: {new_rotation}°)")
                self.files_listbox.selection_set(index)
            else:
                self.files_listbox.delete(index)
                self.files_listbox.insert(index, filename)
                self.files_listbox.selection_set(index)
            
            self.preview_selected_image()
    
    def set_orientation(self, orientation):
        if not self.selected_files:
            messagebox.showinfo("Info", "No files available to change orientation")
            return
            
        total_files = len(self.selected_files)
        confirm = messagebox.askyesno(
            "Confirm Orientation Change", 
            f"Apply {orientation} orientation to all {total_files} images?")
        
        if not confirm:
            return
            
        for i, file_path in enumerate(self.selected_files):
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    is_landscape = width > height
                    
                    if orientation == "landscape":
                        if not is_landscape:
                            self.rotation_info[file_path] = 90
                            self.files_listbox.delete(i)
                            self.files_listbox.insert(i, f"{os.path.basename(file_path)} (Rotated: 90°)")
                        else:
                            self.rotation_info[file_path] = 0
                            self.files_listbox.delete(i)
                            self.files_listbox.insert(i, os.path.basename(file_path))
                    
                    elif orientation == "portrait":
                        if is_landscape:
                            self.rotation_info[file_path] = 90
                            self.files_listbox.delete(i)
                            self.files_listbox.insert(i, f"{os.path.basename(file_path)} (Rotated: 90°)")
                        else:
                            self.rotation_info[file_path] = 0
                            self.files_listbox.delete(i)
                            self.files_listbox.insert(i, os.path.basename(file_path))
            
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't process {os.path.basename(file_path)}: {str(e)}")
        
        if self.files_listbox.curselection():
            self.preview_selected_image()
    
    def preview_selected_image(self):
        selected_indices = self.files_listbox.curselection()
        
        if not selected_indices:
            self.preview_label.config(image='', text="No image selected")
            return
            
        index = selected_indices[0]
        file_path = self.selected_files[index]
        
        try:
            img = Image.open(file_path)
            rotation_angle = self.rotation_info.get(file_path, 0)
            if rotation_angle != 0:
                img = img.rotate(-rotation_angle, expand=True)
            
            preview_width = self.preview_frame.winfo_width()
            preview_height = self.preview_frame.winfo_height()
            
            if preview_width < 50 or preview_height < 50:
                preview_width = 400
                preview_height = 300
            
            img_copy = img.copy()
            img_width, img_height = img.size
            
            width_ratio = preview_width / img_width
            height_ratio = preview_height / img_height
            scale_factor = min(width_ratio, height_ratio) * 0.9
            
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            
            img_copy = img_copy.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_copy)
            
            self.preview_image = img_tk
            self.preview_label.config(image=self.preview_image, text="")
            
            width, height = img.size
            file_size = os.path.getsize(file_path) / 1024
            self.info_label.config(text=f"{os.path.basename(file_path)} | {width}x{height} px | {file_size:.1f} KB")
            
        except Exception as e:
            self.preview_label.config(image='', text="Error loading image")
            messagebox.showerror("Error", f"Couldn't preview image: {str(e)}")
    
    def create_pdf(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No files selected!")
            return
            
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"merged_{timestamp}.pdf"
        
        output_file = filedialog.asksaveasfilename(
            title="Save PDF As",
            defaultextension=".pdf",
            initialfile=default_filename,
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not output_file:
            return
            
        try:
            self.convert_images_to_pdf(self.selected_files, output_file)
            messagebox.showinfo("Success", f"PDF created successfully!\nSaved as: {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create PDF: {str(e)}")
    
    def convert_images_to_pdf(self, image_files, output_pdf):
        images = []
        for img_file in image_files:
            try:
                img = Image.open(img_file)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                    
                rotation_angle = self.rotation_info.get(img_file, 0)
                if rotation_angle != 0:
                    img = img.rotate(-rotation_angle, expand=True)
                
                images.append(img)
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't process {os.path.basename(img_file)}: {str(e)}")
                return
        
        if not images:
            return
        
        try:
            images[0].save(
                output_pdf, 
                "PDF",
                resolution=100.0,
                save_all=True,
                append_images=images[1:],
                quality=95
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create PDF: {str(e)}\n\nTrying alternative method...")
            
            try:
                c = canvas.Canvas(output_pdf, pagesize=letter)
                for img in images:
                    img_width, img_height = img.size
                    pdf_width, pdf_height = letter
                    
                    x_centered = (pdf_width - img_width) / 2
                    y_centered = (pdf_height - img_height) / 2
                    
                    temp_img_path = f"temp_img_{datetime.datetime.now().strftime('%H%M%S%f')}.jpg"
                    img.save(temp_img_path, "JPEG")
                    
                    c.drawImage(temp_img_path, x_centered, y_centered, width=img_width, height=img_height)
                    c.showPage()
                    
                    os.remove(temp_img_path)
                    
                c.save()
            except Exception as e2:
                messagebox.showerror("Error", f"Both PDF creation methods failed: {str(e2)}")
                return

    def on_window_resize(self, event):
        if event.widget == self.root:
            self.preview_selected_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()