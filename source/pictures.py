from PIL import Image
from .settings import MAX_SIGNATURE_HEIGHT, MAX_SIGNATURE_WIDTH


def check_and_resize_image(image_path: str):
    image = Image.open(image_path)

    w, h = image.size
    ratio = h / w

    resized = False

    if w > MAX_SIGNATURE_WIDTH:
        w = MAX_SIGNATURE_WIDTH
        h = int(ratio * w)
        image = image.resize((w, h))
        resized = True

    if h > MAX_SIGNATURE_HEIGHT:
        h = h
        w = int(h / ratio)
        image = image.resize((w, h))
        resized = True

    if resized:
        image.save(image_path)
