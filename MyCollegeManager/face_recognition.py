from PIL import Image


def load_image_file(path):
    return Image.open(path)


def face_locations(image):
    return [(0, 0, 0, 0)] if image is not None else []
