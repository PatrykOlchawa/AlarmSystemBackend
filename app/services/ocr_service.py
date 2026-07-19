import cv2
import pytesseract
import numpy as np
import logging

logger = logging.getLogger(__name__)
class OCRService:
    def read_license_plate(
        self,
        image: str,
    ) -> str | None:
        image = cv2.imread("plate2.png")
        print(type(image))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        text = pytesseract.image_to_string(gray)

        text = text.strip()
        text =  "".join(text.split())
        logger.info(f"Plate: {text}")
        if text == "":
            return None
        
        return text