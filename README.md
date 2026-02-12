# PythonAutoRomTranslator
Python script that automates extraction, translation, and reinsertion of text images using OCR and image processing.

# Overview
PythonAutoRomTranslator scans textures dumped from game ROMs, detects words within textures using an OCR, translates the words, and then generated a new translated image that is dynamically scaled to fit the old image size.
Afterwards it implements the texture into the game.

# Technology Used
- Python 3.11
- Pillow (PIL)
- EasyOCR
- deep-translator

# Status
Early development - core pipeline is funcitonal, optimzation and UI improvements planned.

# Tested On
Windows
(PyCharm Community Edition 2024.3.1.1 used for development)

# Instructions
- Ensure you have the folers and Python script in the same folder.
- Install dependencies.
- Run the python script.
- Translated text will be saved in the "NewTextures" folder

# Future Improvements
- Duplicate texture detection
- Performance optimization
- CLI arguments for path input
- Config file support
- GPU OCR Option
- Error handling
- Broaden reinsertion methods for different types of roms (PSP focused now)

# Author
Davion Franklin

