
# from flask import Flask
from server import (app, jinja2, render_template, request, json, jsonify, datetime,  makeError)

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


from core.logger import logger
from core.response import handle_error

import ntpath

from core.utils import saveImageIOS, printLog


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
@app.route('/face_recognition_func/', methods=['POST'])
@catch_exception
def face_recognition_func():
  if not request.json:
    return json.jsonify(
      username = "",
      password = "",
      status = -1
    )

  data = request.get_json()

  if (data == None):
    logger.insertLog('Exception:', request.remote_addr +  " - " + "not data")
    print("request data none")

    return json.jsonify(
      username = "",
      password = "",
      status = -1
    )
  
  imgstr = re.search(r'base64,(.*)', str(data.get('image_data'))).group(1)   
  detect =  None
  fullname = ""
  token = ""

  if detect.get('status') == 0:
    print('rwere')

  result = {
    "status": detect.get('status'),
    "username": detect.get('username'),
    "fullname": fullname,
    "token": token
  }

  return jsonify(result)
   

  
# =========================================INIT MAIN=========================================
if __name__ == "__main__":

  app.run(host='0.0.0.0', port=8989)

