.# OCR Tool Technical Details
## Project Structure
Main script file: ocr_program_gui.py
## Required Python Version
Python 3.7 or higher is recommended.
## Required Libraries
Install the following libraries using pip:

pip install pytesseract
pip install Pillow
pip install pyautogui
pip install pyperclip
pip install pystray
pip install keyboard

You can install all required libraries at once using the following command:

pip install pytesseract Pillow pyautogui pyperclip pystray keyboard

## Tesseract OCR Installation
1. Download and install Tesseract OCR:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: brew install tesseract
   - Linux: sudo apt-get install tesseract-ocr
2. Ensure the Tesseract executable is in your system PATH or specify its location in the script:
python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust path as needed

## File List
1. ocr_program_gui.py - Main Python script containing the OCR tool code
No additional files are required as the system tray icon is generated programmatically within the script.
## Running the Application
To run the application, navigate to the directory containing ocr_program_gui.py in your terminal or command prompt, then execute:

python ocr_program_gui.py

## System Tray Icon
The system tray icon is created programmatically using the following function in the script:
python
def create_image():
    image = PilImage.new('RGB', (64, 64), color = (73, 109, 137))
    dc = ImageDraw.Draw(image)
    dc.rectangle([20, 20, 44, 44], fill = (255, 255, 255))
    return image

## Global Hotkey
Current global hotkey: Ctrl+Shift+O
Note: This hotkey is currently under review due to potential conflicts with other applications.
## Supported OCR Languages
The current implementation supports the following languages:
- English (eng)
- French (fra)
- German (deu)
- Spanish (spa)
To add more languages, modify the values parameter in the ttk.Combobox initialization:
python
self.language_combo = ttk.Combobox(self.root, textvariable=self.language_var, 
                                   values=["eng", "fra", "deu", "spa"])

Ensure that the corresponding language data files are installed with Tesseract OCR.
## Additional Notes
- The application uses threading to prevent GUI freezing during OCR processing.
- The screen capture functionality uses a full-screen transparent window to allow area selection.
- OCR results are automatically copied to the clipboard for easy pasting.
This technical details file provides all the necessary information for setting up and running the OCR tool project. It includes installation instructions, file structure, and important code snippets for quick reference.