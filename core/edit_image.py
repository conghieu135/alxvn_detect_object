import numpy as np
from PIL import Image, ImageDraw, ExifTags



def load_image_file(file_path, mode='RGB'):
    """
      Loads an image file (.jpg, .png, etc) into a numpy array

      :param file: image file name or file object to load
      :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
      :return: image contents as numpy array
      """
    pil_image = Image.open(file_path)
    
    # if mode:
    #     pil_image = pil_image.convert(mode)

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    if pil_image._getexif() == None:
        if mode:
            pil_image = pil_image.convert(mode)
        return np.array(pil_image)

    exif = dict(pil_image._getexif().items())

    image = pil_image
    if orientation in exif:
        if exif[orientation] == 3:
            image = pil_image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = pil_image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = pil_image.rotate(90, expand=True)

    image = image.convert(mode)

    # cv2.imshow("check", np.array(image))
    # cv2.waitKey(0)

    return np.array(image)



def load_image_file_2(file_path, mode='RGB'):
    """
      Loads an image file (.jpg, .png, etc) into a numpy array

      :param file: image file name or file object to load
      :param mode: format to convert the image to. Only 'RGB' (8-bit RGB, 3 channels) and 'L' (black and white) are supported.
      :return: image contents as image
      """
    pil_image = Image.open(file_path)
    
    # if mode:
    #     pil_image = pil_image.convert(mode)

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    if pil_image._getexif() == None:
        if mode:
            pil_image = pil_image.convert(mode)
        return  pil_image

    exif = dict(pil_image._getexif().items())

    image = pil_image
    if orientation in exif:
        if exif[orientation] == 3:
            image = pil_image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = pil_image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = pil_image.rotate(90, expand=True)

    image = image.convert(mode)

    # cv2.imshow("check", np.array(image))
    # cv2.waitKey(0)

    return image