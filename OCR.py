import cv2
import pytesseract
import numpy as np
from PIL import Image
from pdf2image import convert_from_path  # Рендеринг PDF


class OCR:
    def __init__(self, tesseract_path):
        self.tesseract_path = tesseract_path
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path

    def PreprocessImage(self, img):
        gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)  # Перевод в оттенки серого
        gray = cv2.medianBlur(gray, 3)  # Удаление шумов
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Бинаризация
        return binary

    def ConvertPDF(self, lang, file, resname):
        images = convert_from_path(file, dpi=300)  # Увеличение DPI для лучшего качества
        pages_text = [
            f"\n=== Страница {i + 1} ===\n\n" + pytesseract.image_to_string(self.PreprocessImage(img), lang=lang)
            for i, img in enumerate(images) ]

        with open(f"{resname}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(pages_text))

    def ConvertImage(self, lang, file, resname):
        imgCV = cv2.imread(file)
        imgPostProcess = self.PreprocessImage(imgCV)
        text = pytesseract.image_to_string(imgPostProcess, lang=lang)
        with open(f'{resname}.txt', mode='w') as f:
            f.write(text)

"""ocr = OCR("D:/NLP_GI/Tesseract-OCR/tesseract.exe")
ocr.ConvertPDF("rus", "test.pdf", "test")
"""