import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import qrcode
import os

class PosterQRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PosterQR Pro - Python Edition")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f0f0f0")

        # --- State Variables ---
        self.base_image_path = None
        self.base_image = None  # The full resolution PIL Image
        self.display_image = None # The resized PIL Image for display
        self.tk_image = None      # The ImageTk object for the canvas
        
        # Defaults matching the web app
        self.qr_content = tk.StringVar(value="https://openai.com")
        self.qr_size_percent = tk.DoubleVar(value=25.0)
        self.qr_x_percent = tk.DoubleVar(value=50.0)
        self.qr_y_percent = tk.DoubleVar(value=45.0)
        self.fg_color = "#E9F6F1"
        self.bg_color = "#15382C"

        # UI Layout
        self.create_sidebar()
        self.create_canvas_area()

    def create_sidebar(self):
        # Sidebar Frame
        sidebar = tk.Frame(self.root, width=300, bg="white", padx=20, pady=20)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False) # Fix width

        # Title
        tk.Label(sidebar, text="PosterQR", font=("Helvetica", 16, "bold"), bg="white").pack(anchor="w", pady=(0, 20))

        # 1. Upload Section
        tk.Label(sidebar, text="1. BASE IMAGE", font=("Helvetica", 10, "bold"), fg="gray", bg="white").pack(anchor="w")
        btn_upload = ttk.Button(sidebar, text="Upload Poster", command=self.load_image)
        btn_upload.pack(fill="x", pady=(5, 20))

        # 2. Content Section
        tk.Label(sidebar, text="2. QR CONTENT", font=("Helvetica", 10, "bold"), fg="gray", bg="white").pack(anchor="w")
        entry_url = tk.Entry(sidebar, textvariable=self.qr_content, font=("Helvetica", 10), bd=1, relief="solid")
        entry_url.pack(fill="x", pady=(5, 5), ipady=4)
        entry_url.bind("<KeyRelease>", self.update_preview) # Live update

        # 3. Controls Section
        tk.Label(sidebar, text="3. POSITION & STYLE", font=("Helvetica", 10, "bold"), fg="gray", bg="white").pack(anchor="w", pady=(15, 5))

        # Size Slider
        tk.Label(sidebar, text="Size (%)", bg="white").pack(anchor="w")
        scale_size = ttk.Scale(sidebar, variable=self.qr_size_percent, from_=5, to=80, command=self.update_preview)
        scale_size.pack(fill="x", pady=(0, 10))

        # X Position Slider
        tk.Label(sidebar, text="Position X (%)", bg="white").pack(anchor="w")
        scale_x = ttk.Scale(sidebar, variable=self.qr_x_percent, from_=0, to=100, command=self.update_preview)
        scale_x.pack(fill="x", pady=(0, 10))

        # Y Position Slider
        tk.Label(sidebar, text="Position Y (%)", bg="white").pack(anchor="w")
        scale_y = ttk.Scale(sidebar, variable=self.qr_y_percent, from_=0, to=100, command=self.update_preview)
        scale_y.pack(fill="x", pady=(0, 20))

        # Colors
        color_frame = tk.Frame(sidebar, bg="white")
        color_frame.pack(fill="x", pady=(0, 20))
        
        # FG Color Button
        self.btn_fg = tk.Button(color_frame, text="QR Color", bg=self.fg_color, fg="black", command=lambda: self.pick_color('fg'), relief="flat", width=12)
        self.btn_fg.pack(side="left", padx=(0, 5))
        
        # BG Color Button
        self.btn_bg = tk.Button(color_frame, text="Bg Color", bg=self.bg_color, fg="white", command=lambda: self.pick_color('bg'), relief="flat", width=12)
        self.btn_bg.pack(side="right", padx=(5, 0))

        # Download Button
        self.btn_save = tk.Button(sidebar, text="Download Poster", command=self.save_image, bg="black", fg="white", font=("Helvetica", 10, "bold"), pady=10, relief="flat", state="disabled")
        self.btn_save.pack(side="bottom", fill="x")

    def create_canvas_area(self):
        # Main display area
        self.canvas_frame = tk.Frame(self.root, bg="#e5e5e5")
        self.canvas_frame.pack(side="right", fill="both", expand=True)

        # Canvas for drawing the image
        self.canvas = tk.Canvas(self.canvas_frame, bg="#e5e5e5", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Placeholder text
        self.canvas.create_text(300, 300, text="Please upload an image", fill="gray", font=("Helvetica", 14))

        # Bind window resize to update preview
        self.root.bind("<Configure>", self.on_resize)

    def pick_color(self, target):
        color = colorchooser.askcolor(title="Choose Color")[1]
        if color:
            if target == 'fg':
                self.fg_color = color
                self.btn_fg.config(bg=color)
            else:
                self.bg_color = color
                self.btn_bg.config(bg=color)
            self.update_preview()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.base_image_path = file_path
            try:
                self.base_image = Image.open(file_path).convert("RGBA")
                self.btn_save.config(state="normal", bg="black")
                self.update_preview()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def generate_qr_image(self, size_px):
        # Generate QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=1, # Small border for the QR itself, we add custom padding later
        )
        qr.add_data(self.qr_content.get())
        qr.make(fit=True)

        # Convert colors to RGB tuples
        try:
            # Simple hex to RGB conversion if needed, but make_image handles hex strings usually
            img_qr = qr.make_image(fill_color=self.fg_color, back_color=self.bg_color).convert("RGBA")
        except:
            # Fallback if color format issues
            img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

        # Resize to target size (high quality)
        img_qr = img_qr.resize((size_px, size_px), Image.Resampling.LANCZOS)
        
        # Add padding (the wrapper style from web app)
        padding = int(size_px * 0.05) # 5% padding
        final_size = size_px + (padding * 2)
        
        bg_square = Image.new("RGBA", (final_size, final_size), self.bg_color)
        
        # Paste QR onto the colored square
        bg_square.paste(img_qr, (padding, padding), img_qr)
        
        return bg_square

    def get_composed_image(self, base_img):
        """
        Composes the QR code onto the provided base_img.
        Used for both Preview (resized base) and Save (original base).
        """
        if not base_img:
            return None
            
        working_img = base_img.copy()
        width, height = working_img.size
        
        # Calculate QR dimensions based on percentage of base image width
        qr_display_size = int((self.qr_size_percent.get() / 100) * width)
        if qr_display_size < 10: qr_display_size = 10
        
        qr_img = self.generate_qr_image(qr_display_size)
        
        # Calculate Position
        # Coordinates are center-based in logic: (X% * width) - (qr_width / 2)
        pos_x = int((self.qr_x_percent.get() / 100) * width) - (qr_img.width // 2)
        pos_y = int((self.qr_y_percent.get() / 100) * height) - (qr_img.height // 2)
        
        # Paste with alpha channel
        working_img.paste(qr_img, (pos_x, pos_y), qr_img)
        
        return working_img

    def update_preview(self, event=None):
        if not self.base_image:
            return

        # Calculate resize factor to fit canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width < 10 or canvas_height < 10: return # Wait for window to init

        img_w, img_h = self.base_image.size
        ratio = min(canvas_width/img_w, canvas_height/img_h)
        new_size = (int(img_w * ratio), int(img_h * ratio))
        
        # Resize base image for preview performance
        preview_base = self.base_image.resize(new_size, Image.Resampling.LANCZOS)
        
        # Compose on the resized preview base
        # NOTE: We cannot just compose on full res and resize, it's too slow for sliders.
        # We must simulate the composition on the small image.
        
        # We need to pass the Preview Base, BUT we need to temporarily adjust 
        # the logic in get_composed_image to handle the fact that this image is smaller.
        # Actually, logic handles percentage, so it should just work! 
        
        final_preview = self.get_composed_image(preview_base)
        
        # Update Canvas
        self.tk_image = ImageTk.PhotoImage(final_preview)
        self.canvas.delete("all")
        # Center in canvas
        x_center = canvas_width // 2
        y_center = canvas_height // 2
        self.canvas.create_image(x_center, y_center, image=self.tk_image, anchor="center")

    def on_resize(self, event):
        # Debounce resize slightly or just handle specific widget
        if event.widget == self.canvas:
            self.update_preview()

    def save_image(self):
        if not self.base_image:
            return
            
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if save_path:
            try:
                # Compose on the FULL resolution image
                final_img = self.get_composed_image(self.base_image)
                final_img.save(save_path)
                messagebox.showinfo("Success", "Poster saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PosterQRApp(root)
    root.mainloop()