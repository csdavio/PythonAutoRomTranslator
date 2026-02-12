"""
Author: Davion Franklin <csdavio>
@Date: 2026-01-14
@Email: davionfranklin2004@gmail.com
@LastUpdate: 2026-02-01

Description:
Automates extraction, translation, and reinsertion of in-game text 
from dumped ROM textures using OCR and image processing.

Dependencies:
 - Pillow (PIL)
 - EasyOCR
 - deep-translator
 -os (standard library)
"""

#TODO:
# Add error handling.
# Implement logging for translated text.
# Implement GPU usage.
# Add ability to manually assign translation for incorrect translations.

from PIL import Image, ImageDraw, ImageFont
import easyocr
from deep_translator import GoogleTranslator
import os

# Creates OCRReader object.
reader = easyocr.Reader(['en', 'ja'], gpu=False)  # Initiate the OCR and languages.

# Reference to path with textures.
sample_textures_path = 'SampleTextures/'  # TODO: Replace hardcoded paths.
black_bg_path = 'BlackBG/'
new_textures_path = 'NewTextures/'

def run_ocr(ocr_reader, textures_path:str):
    return ocr_reader.readtext(textures_path)

# Prints translated text to console.
def translate_words(japanese_text:str):
    translated_text = GoogleTranslator(source='auto', target='en').translate(japanese_text)
    print(f'Translation successful! {japanese_text} --> {translated_text}.\n')
    return translated_text

# Copies transparent image and pastes it on top of created Black background for easier OCR reading.
def bg_to_black(texture:str):
    transparent_image = Image.open(sample_textures_path + texture)

    black_bg = Image.new('RGB', transparent_image.size, (0,0,0))
    black_bg.paste(transparent_image, mask=transparent_image.split()[3])

    black_bg_texture_path = sample_textures_path + black_bg_path + texture
    black_bg.save(black_bg_texture_path)

    return black_bg_texture_path

def check_for_transparency(textures_path:str):
    image = Image.open(textures_path)
    rgb_data = image.getdata()

    if image.mode != 'RGBA': # Returns false is image has no transparency.
        return False

    # If RGB values are not all 255 then image is not greyscale; ignores.
    for r, g, b, a in rgb_data:
        if r != g or g != b:
            return False

    return True

# Creates image with translated text referencing its original texture's image size.
def generate_image(textures_path:str, new_textures_folder:str, translated_text:str):
    reference_image = Image.open(textures_path)
    width, height = reference_image.size

    # Dynamically adjust height to fit image based on amount of characters in translated string.
    # TODO: add upper and lower limits.
    # TODO: account for image size.

    BASE_FONT_SIZE = 28
    BASE_CHAR_COUNT = 10

    char_count = 0
    for char in translated_text:
        char_count += 1

    char_count_ratio = BASE_CHAR_COUNT/char_count
    font_size = int(BASE_FONT_SIZE * char_count_ratio)

    font = ImageFont.truetype("CalibriBold.ttf", font_size)
    new_image = Image.new('RGBA', (width,height),(0,0,0,0))
    translated_image = ImageDraw.Draw(new_image)


    translated_image.text(xy=(0,0), text=translated_text, fill=(255,255,255), font=font, anchor='lt',spacing=0,
                          align= 'left', direction=None, features=None, language=None, stroke_width=0, stroke_fill=None,
                          embedded_color=False, font_size=25)

    print(f'Image: "{translated_text}.png" has been saved successfully to path "{new_textures_folder}".\n')

    return new_image.save(new_textures_folder+translated_text.replace(' ','')+'.png')

def check_if_square_texture(path):
    image = Image.open(path)
    if image.size[0] == image.size[1]: # Checks if height and width of image are equal (square image)
        return True
    return False

def main():

    # Iterates through folder with textures and translates images.
    # Will need to optimize, to avoid duplicate textures, and delete not text images for accessibility.
    for image in os.listdir(sample_textures_path):
        # Skips non image files within the set path.
        if not image.lower().endswith(('.png', 'jpg', 'jpeg', '.bmp')):
            continue

        texture_path = sample_textures_path + image
        if not check_if_square_texture(texture_path):
            black_bg_texture_path = bg_to_black(str(image))
            ocr_result = run_ocr(reader,black_bg_texture_path)

            if ocr_result:
                japanese_words = ocr_result[0][1]
                translated_text = translate_words(japanese_words)
                generate_image(texture_path, new_textures_path, translated_text)

main()




