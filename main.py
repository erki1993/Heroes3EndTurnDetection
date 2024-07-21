import cv2
from PIL import ImageGrab, Image
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
END_TURN_SAMPLE_IMAGE = "EndTurnSample.png"


def get_image_similiarity(sample_picture_file, new_picture_file):
    # Load images
    image1 = cv2.imread(sample_picture_file)
    image2 = cv2.imread(new_picture_file)
    hist_img1 = cv2.calcHist([image1], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist_img1[255, 255, 255] = 0  # ignore all white pixels
    cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    hist_img2 = cv2.calcHist([image2], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    hist_img2[255, 255, 255] = 0  # ignore all white pixels
    cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
    # Find the metric value
    metric_val = round(cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL), 2)
    print(f"Similarity Score for image {new_picture_file}: ", metric_val)
    return metric_val


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        im = ImageGrab.grab()
        im.save("Screenshot.png")
        similiarity = get_image_similiarity(END_TURN_SAMPLE_IMAGE, "Screenshot.png")
        if similiarity == 1.0:
            print("END TURN detected")
            image = cv2.imread("Screenshot.png")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            filename = "Screenshot.png"
            cv2.imwrite(filename, gray)

            text = pytesseract.image_to_string(Image.open("Screenshot.png"), lang='eng')
            print("Read out text", text)
            break
        time.sleep(1)
