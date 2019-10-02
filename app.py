
# from flask import Flask
from server import (app, jinja2, render_template, request, json, jsonify,  makeError)

import os
import os.path
import io
import cv2
import time
import base64
import re
import argparse
import ssl
from functools import wraps
from datetime import datetime

from core.logger import logger
from core.response import handle_error

import ntpath

from core.utils import saveImageIOS, printLog, saveImage
from model.detect_object import DETECT_OBJECT 

import base64

from core.string_resource import StringResource

# ===========construct the argument parser and parse the arguments===========
ap = argparse.ArgumentParser()

# thời gian chờ tối đa để nhận diện khuôn mặt (milisecond)
ap.add_argument("-time", "--time_waiting", type=int, default=15000 ,
	help="Maximum standby time for face recognition")

# thời gian lấy hình định kì để gửi lên server xác nhận khuôn mặt (milisecond)
ap.add_argument("-duration", "--duration_waiting", type=int, default=1000,
	help="Time to periodically upload images to send to face confirmation server")

# số lần sai cho phép khi phát hiện khuôn mặt sai (không tính số lần không tìm thấy khuôn mặt, hoặc tìm thấy nhiều khuôn mặt)
ap.add_argument("-co", "--count_fail_valid", type=int, default=10,
	help="The number of false positives allowed when false faces are detected")

# số ảnh tối đa để train cho một user
ap.add_argument("-ma", "--max_image_user", type=int, default=10,
	help="So anh toi da de train 1 user tu web")


args = vars(ap.parse_args())


# ====================================2019-07-15============================================
def createFolder(folderPath):
  directory_image = os.getcwd() + "/" + folderPath

  if not os.path.exists(directory_image):
    os.makedirs(directory_image)

folderNameImage = "image_receive"
folderNameResultImage = "image_result"

createFolder(folderNameImage)
createFolder(folderNameResultImage)
# ==========================================================================================

detect_object_obj = DETECT_OBJECT()


# =========================================LINK PAGE=========================================
def catch_exception(func):
  @wraps(func)
  def decorated_function(*args, **kwargs):
    try:
      return func(*args, **kwargs)
    except Exception as e:
      logger.insertLog('Exception:', makeError(e))
      return handle_error(e)
  
  return decorated_function


# =========================================LINK API=========================================
@app.route('/detect_object_api/', methods=['POST'])
@catch_exception
def detect_object_func():
  if not request.json:
    return json.jsonify(
      status = False,
      message = "Data is none"
    )

  data = request.get_json()

  if (data == None):
    logger.insertLog('Exception:', request.remote_addr +  " - " + "not data")
    print("request data none")

    return json.jsonify(
      status = False,
      message = "Data is none"
    )

  imgstr = data.get('image_data')
  dt = datetime.now()
  
  model = int(data.get('model'))

  filename = time.strftime('%Y%m%d%H%M%S') + str(dt.microsecond)
  imgPath = os.getcwd() + "/" + folderNameImage + "/" +  filename + ".jpg"

  saveImage(imgstr, imgPath)

  imgPathResult = os.getcwd() + "/" + folderNameResultImage + "/" +  filename + "_result" + ".jpg"
  img, arr_labels = detect_object_obj.detect_object(imgPath, imgPathResult, model)
  

  if len(arr_labels) < 1:
    result = {
      "status": True,
      "message": StringResource.MSG_CANNOT_FOUND_OBJECT,
      "count": 0
    }

    return jsonify(result)


  # message = "There are " + str(len(arr_labels)) + " object " + ("" if len(arr_labels)==1 else "s") +  " in image: "

  message = "画像には" + str(len(arr_labels)) + "つのオブジェクトがあります："
  
  seperator = ', '

  message += seperator.join(arr_labels)

  with open(imgPathResult, "rb") as idol_img_file:
      base64IdolStr = base64.b64encode(idol_img_file.read()).decode('ascii')

  result = {
    "status": True,
    "message": message,
    "count": len(arr_labels),
    "imgResult": base64IdolStr
  }

  return jsonify(result)
   

  
# =========================================INIT MAIN=========================================
if __name__ == "__main__":

  # imgPath = os.getcwd() + "/" + folderNameImage + "/" +  "20190919092123669510.jpg"
  # imgPathResult = os.getcwd() + "/" + folderNameResultImage + "/" +  "test" + "_result" + ".jpg"
  # img, arr_labels = detect_object_obj.detect_object(imgPath, imgPathResult)
  
  # cv2.imshow('image',img)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()


  app.run(host='0.0.0.0', port=8989)

