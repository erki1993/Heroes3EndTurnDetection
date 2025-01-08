import cv2
from PIL import ImageGrab, Image
import time
import pytesseract
import logging
from discord import SyncWebhook
from settings import DISCORD_WEBHOOK, TESSERACT_PATH, MIN_SIMILIAIRTY, SLEEP_TIME_SECONDS

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
END_TURN_SAMPLE_IMAGE = "EndTurnSampleHD.png"
SCREENSHOT_FILE = "Screenshot.png"
SCREESHOT_CROPPED_FILE = "Screenshot_crop.png"


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
    logging.info(f"Similarity Score for image {new_picture_file}: {metric_val}")
    return metric_val


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    detected = False
    last_sent_user = None
    last_detected_text = None
    while True:
        try:
            im = ImageGrab.grab()
        except OSError as e:
            logging.error(e)
            time.sleep(SLEEP_TIME_SECONDS)
            continue
        im.save(SCREENSHOT_FILE)
        similiarity = get_image_similiarity(END_TURN_SAMPLE_IMAGE, SCREENSHOT_FILE)
        if similiarity >= MIN_SIMILIAIRTY and detected is False:
            detected = True
            logging.info("END TURN detected")
            im = Image.open(SCREENSHOT_FILE)
            width, height = im.size
       
            left = width / 3 + 140
            top = height / 3 + 30
            right = (2 * width / 3) - 140
            bottom = (2 * height / 3) - 250
            im = im.crop((left, top, right, bottom))
            im.save(SCREESHOT_CROPPED_FILE)

            text = pytesseract.image_to_string(Image.open(SCREESHOT_CROPPED_FILE), lang='eng')
            logging.info(f"Read out text from image: {text}")

            if last_detected_text == text:
                logging.info("Text not changed")
            else:
                last_detected_text = text
                if "attack" in text:
                    # in case someone is attacked outside of normal turn order
                    logging.info(text)                    
                    webhook = SyncWebhook.from_url(DISCORD_WEBHOOK)
                    webhook.send(text)
                    logging.info("Sent message to Discord")
                elif "turn" in text:
                    player_name = text.split("'s turn")[0]
                    logging.info(text)
                    if last_sent_user != player_name:
                        last_sent_user = player_name
                        webhook = SyncWebhook.from_url(DISCORD_WEBHOOK)
                        webhook.send(text)
                        logging.info("Sent message to Discord")
                    else:
                        logging.debug(f"Already sent for player {player_name}")
        else:
            logging.debug(f"Similiarity too low: {similiarity}")
            detected = False
        time.sleep(SLEEP_TIME_SECONDS)
