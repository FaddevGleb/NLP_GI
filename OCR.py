import cv2
import pytesseract
import numpy as np
import fitz  # PyMuPDF
from PIL import Image


class OCR:
    def __init__(self, path):
        self.path = path
        pytesseract.pytesseract.tesseract_cmd = fr'{self.path}'

    def adjust_contrast_brightness(self, img, contrast: float = 1.0, brightness: int = 0):
        brightness += int(round(255 * (1 - contrast) / 2))
        return cv2.addWeighted(img, contrast, img, 0, brightness)

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
                img = img.resize((2000, 2000))
                open_cv_image = np.array(img)
                grayImage = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2GRAY)
                contrastAdjustedImage = self.adjust_contrast_brightness(grayImage, 0.9, 20)
                #threshold, binarizedImage = cv2.threshold(contrastAdjustedImage, 128, 255, cv2.THRESH_OTSU)
                #binarizedContrastAdjustedImage = self.adjust_contrast_brightness(binarizedImage, 2, 1)
                cv2.imwrite(f"{page_num}.png",contrastAdjustedImage)
                pageText = pytesseract.image_to_string(contrastAdjustedImage, lang=lang)
                PDFtext += pageText
            doc.close()
            f.write(PDFtext)



ocr = OCR("D:/NLP_GI/Tesseract-OCR/tesseract.exe")
ocr.ConvertPDF("rus", "PDT.pdf", "ConvertedPDF")
