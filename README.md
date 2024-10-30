# OCR Tool Technical Details

A Python-based OCR tool that lives in your system tray and captures text from screen selections.

## Required Python Version
Python 3.7 or higher is recommended.

## Required Libraries
Install the following libraries:
```
pip install pytesseract Pillow pyautogui pyperclip pystray keyboard
```

## Tesseract OCR Installation
1. Download and install Tesseract OCR:
   - Windows: https://github.com/UB-Mannheim/tesseract/wiki
   - macOS: `brew install tesseract`
   - Linux: `sudo apt-get install tesseract-ocr`

## How to Run
```
python ocr_program_gui.py
```

## Features
- System tray integration
- Global hotkey (Ctrl+Shift+O)
- Supports multiple languages (English, French, German, Spanish)
- Auto-copies results to clipboard
- Screen area selection tool

## Note
Make sure Tesseract is in your system PATH or specify its location in the script.