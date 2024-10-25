import pytesseract
from PIL import Image
import pyautogui
import pyperclip
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import pystray
from pystray import MenuItem as item
from PIL import Image as PilImage, ImageDraw
import keyboard

def create_image():
    # Create a simple icon
    image = PilImage.new('RGB', (64, 64), color = (73, 109, 137))
    dc = ImageDraw.Draw(image)
    dc.rectangle([20, 20, 44, 44], fill = (255, 255, 255))
    return image

class OCRApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("OCR Tool")
        self.root.geometry("300x200")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.label = ttk.Label(self.root, text="OCR Tool")
        self.label.pack(pady=10)

        self.language_var = tk.StringVar(value="eng")
        self.language_label = ttk.Label(self.root, text="OCR Language:")
        self.language_label.pack()
        self.language_combo = ttk.Combobox(self.root, textvariable=self.language_var, 
                                           values=["eng", "fra", "deu", "spa"])
        self.language_combo.pack(pady=5)

        self.start_button = ttk.Button(self.root, text="Start OCR", command=self.start_ocr)
        self.start_button.pack(pady=10)

        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var)
        self.status_label.pack(pady=10)

        self.capture_complete = threading.Event()
        self.region = None

        # Create system tray icon
        image = create_image()
        menu = (item('Show', self.show_window), item('Quit', self.quit_app))
        self.icon = pystray.Icon("name", image, "OCR Tool", menu)

        # Set up global hotkey
        keyboard.add_hotkey('ctrl+shift+o', self.start_ocr)

    def run(self):
        threading.Thread(target=self.icon.run, daemon=True).start()
        self.root.withdraw()  # Start with the window hidden
        self.root.mainloop()

    def show_window(self):
        self.root.deiconify()

    def hide_window(self):
        self.root.withdraw()

    def quit_app(self):
        self.icon.stop()
        self.root.quit()

    def start_ocr(self):
        self.status_var.set("Select area on screen...")
        self.root.withdraw()
        self.capture_complete.clear()
        threading.Thread(target=self.perform_ocr, daemon=True).start()
        self.root.after(100, self.capture_screen_region)

    def perform_ocr(self):
        self.capture_complete.wait()
        self.status_var.set("Performing OCR...")
        screenshot = pyautogui.screenshot(region=self.region)
        
        text = pytesseract.image_to_string(screenshot, lang=self.language_var.get())
        
        pyperclip.copy(text)
        
        self.root.after(0, self.show_result, text)

    def capture_screen_region(self):
        root = tk.Toplevel(self.root)
        root.attributes('-fullscreen', True)
        root.attributes('-alpha', 0.3)
        root.configure(background='grey')

        canvas = tk.Canvas(root, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        start_x, start_y = 0, 0
        rect = None

        def on_mouse_press(event):
            nonlocal start_x, start_y, rect
            start_x, start_y = event.x, event.y
            if rect:
                canvas.delete(rect)
            rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)

        def on_mouse_move(event):
            nonlocal rect
            if rect:
                canvas.delete(rect)
            rect = canvas.create_rectangle(start_x, start_y, event.x, event.y, outline='red', width=2)

        def on_mouse_release(event):
            nonlocal rect
            if rect:
                canvas.delete(rect)
            x1, y1 = start_x, start_y
            x2, y2 = event.x, event.y
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            self.region = (x1, y1, x2-x1, y2-y1)
            root.destroy()

        canvas.bind('<ButtonPress-1>', on_mouse_press)
        canvas.bind('<B1-Motion>', on_mouse_move)
        canvas.bind('<ButtonRelease-1>', on_mouse_release)

        root.focus_force()
        root.grab_set()
        root.wait_window(root)

        self.capture_complete.set()

    def show_result(self, text):
        self.status_var.set("OCR completed")
        messagebox.showinfo("OCR Result", f"Text copied to clipboard:\n\n{text[:500]}...")

if __name__ == "__main__":
    app = OCRApp()
    app.run()