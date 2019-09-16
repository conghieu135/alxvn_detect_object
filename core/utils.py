import os, shutil, re, datetime, base64
from PIL import Image, ImageDraw, ExifTags
import PIL.Image
import numpy as np
import io
from PIL import Image, ImageDraw, ExifTags, ImageOps
from io import BytesIO
import traceback

TEMP_PATH = 'tmp'
FULL_PATH = ''
TRAIN_PATH = 'alx_examples'
SUB_IMG = 'train'


def checkIsExit(_path):
  return os.path.isdir(_path)

def makeDir(root=0, subpath=""):  
  """
    Make folder
    Parameters: 
      root: folder root: (1. TEMP_PATH, 2. TRAIN_PATH, other: Subpath)
      subpath: sub folder
    Returns: none
  """
  if root == 1 :
    if not checkIsExit(TEMP_PATH):
      os.makedirs(TEMP_PATH)
    FULL_PATH = os.path.join(TEMP_PATH, subpath)
  elif root == 2:
    if not checkIsExit(TRAIN_PATH):
      os.makedirs(TRAIN_PATH)
    subtrain = os.path.join(TRAIN_PATH, SUB_IMG)
    if not checkIsExit(subtrain):
      os.makedirs(subtrain)
    FULL_PATH = os.path.join(subtrain, subpath)
  else:
    FULL_PATH = subpath
  if not checkIsExit(FULL_PATH):
    os.makedirs(FULL_PATH)
  return FULL_PATH

def deleteTmpFolder():
  """
    Descriptions: Delete all subfolder from parameter
    Parameters:
      none
  """
  for itm in os.listdir(TEMP_PATH):
    path_str = os.path.join(TEMP_PATH, itm)
    try:
      if os.path.isfile(path_str):
        os.unlink(path_str)
      elif os.path.isdir(path_str):
        shutil.rmtree(path_str)
    except Exception as e:
      print(e)

def moveFile(source='', dst='', username=''):
  if not source:
    source = TEMP_PATH
  if not dst:
    dst = os.path.join(TRAIN_PATH, SUB_IMG)
  if checkIsExit(TEMP_PATH):
    for itm in os.listdir(TEMP_PATH):
      src = os.path.join(TEMP_PATH, itm)
      if checkIsExit(os.path.join(dst, itm)):
        copyFile(src, os.path.join(dst, itm))
      else:        
        makeDir(2, itm)
        copyFile(src, os.path.join(dst, itm))
  # Delete Folder after copy to dst
  deleteTmpFolder()
  return dst + "/" + username

def copyFile(folder, dst):
  for file in os.listdir(folder):
    src = os.path.join(folder, file)
    if(os.path.isfile(src)):
      shutil.copy(src, dst)

def makeFile(data='', UserId='', idx=0, is_iOS=False):
  """
    Description:
    Parameters:

  """
  index =  str(idx).zfill(2)
 
  filename = UserId + '_' + index + ct.EXTENDSION_IMAGE
  prefix = makeDir(1, UserId)
  file_path = os.path.join(prefix, filename)
  
  if is_iOS:
    saveImageIOS(data, file_path)
  else:
    saveImage(data, file_path)

  return file_path

def saveImage(data='', file_path=''):
  data = base64.b64decode(str(data))
  image = Image.open(io.BytesIO(data)).convert("RGB")
  image.save(file_path, optimize=True, quality=95)

def saveImageIOS(data='', file_path=''):
  data = base64.b64decode(str(data))
  image = Image.open(io.BytesIO(data)).convert("RGB")
  image = ImageOps.mirror(image)
  image.save(file_path, optimize=True, quality=95)

def printLog(msg): 
  isDebug = False
  if isDebug:
    print(msg)


def makeError(error):
  # message = [str(x) for x in error.args]
  err = traceback.format_exc()
  return err

def convertImg(url):
    image_file = Image.open(url)
    mode='RGB'
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    if image_file._getexif() != None:
      exif = dict(image_file._getexif().items())
      if orientation in exif:
          if exif[orientation] == 3:
              image_file = image_file.rotate(180, expand=True)
          elif exif[orientation] == 6:
              image_file = image_file.rotate(270, expand=True)
          elif exif[orientation] == 8:
              image_file = image_file.rotate(90, expand=True)
    image_file = image_file.convert(mode)
    buffered = BytesIO()
    image_file.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str.decode("utf-8")


def indent(text, amount, ch=' '):
  padding = amount * ch
  return ''.join(padding+line for line in text.splitlines(True))