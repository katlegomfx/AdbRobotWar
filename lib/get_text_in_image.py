import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

def text(file='./data/battle.png'):
    text = pytesseract.image_to_string(file)
    print(text)
    return text