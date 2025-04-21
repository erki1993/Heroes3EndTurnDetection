import os

from main import read_text_from_image, crop_image_for_tesseract

ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets')


def test_read_erik_turn_text():
    image_path = os.path.join(ASSETS_DIR, 'Erik.png')
    cropped_image = crop_image_for_tesseract(image_path)
    text = read_text_from_image(cropped_image)
    print(f"Read out text: {text}")
    assert "Erik's turn." == text, f"OCR failed. Got: {text}"


def test_read_attack_text():
    image_path = os.path.join(ASSETS_DIR, 'GrailHunter.png')
    cropped_image = crop_image_for_tesseract(image_path)
    text = read_text_from_image(cropped_image)
    print(f"Read out text: {text}")
    assert "Carl the GrailHunter's Hero is under attack!" == text, f"OCR failed. Got: {text}"


def test_palyerads_turn():
    # this does not work yet
    image_path = os.path.join(ASSETS_DIR, 'EndTurnSample.png')
    cropped_image = crop_image_for_tesseract(image_path)
    text = read_text_from_image(cropped_image)
    print(f"Read out text: {text}")
    assert "Playerads's turn." == text, f"OCR failed. Got: {text}"


def test_kevins_turn():
    image_path = os.path.join(ASSETS_DIR, 'EndTurnSampleHD.png')
    cropped_image = crop_image_for_tesseract(image_path)
    text = read_text_from_image(cropped_image)
    print(f"Read out text: {text}")
    assert "Kevin's turn." == text, f"OCR failed. Got: {text}"