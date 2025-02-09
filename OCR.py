import cv2
import pytesseract
import numpy as np
import fitz  # PyMuPDF
from PIL import Image


class OCR:
    def __init__(self, path):
        self.path = path
        pytesseract.pytesseract.tesseract_cmd = fr'{self.path}'

    def ConvertImage(self, lang, file, resname):
        img_cv = cv2.imread(file)
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(img_rgb, lang=lang)
        with open(f'{resname}.txt', mode='w') as f:
            f.write(text)

    def ConvertPDF(self, lang, file, resname):
        PDFtext = ""
        with open(f'{resname}.txt', mode='w') as f:
            doc = fitz.open(file)

            for page_num in range(doc.page_count):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                open_cv_image = np.array(img)
                PageText = pytesseract.image_to_string(open_cv_image, lang=lang)
                PDFtext += PageText
            doc.close()
            f.write(PDFtext)

"""
ocr = OCR("D:/NLP_GI/Tesseract-OCR/tesseract.exe")
ocr.ConvertPDF("eng", "test.pdf", "ConvertedPDF")
"""