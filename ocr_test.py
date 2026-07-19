import cv2
import pytesseract    
image = cv2.imread("plate.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
text = pytesseract.image_to_string(gray)

text = text.strip()
text =  "".join(text.split())
print(f"Plate number: {text}")
        
