import numpy as np
import argparse
import cv2 as cv
import subprocess
import time
import os
from model.yolo_util import infer_image, show_image

class DETECT_OBJECT:
	def __init__(self):

		# label_path= "./model/coco-labels"
		# config_path = "./model/yolov3.cfg"
		# weight_path = "./model/yolov3.weights"

		label_path= "./model/clock-glass-laptop"
		config_path = "./model/clock_glass_laptop.cfg"
		weight_path = "./model/clock_glass_laptop_5000.weights"

		self.confidence = 0.5
		self.threshold = 0.3
		self.showtime = False

		# Get the labels
		self.labels = open(label_path).read().strip().split('\n')
		
		# Load the weights and configutation to form the pretrained YOLOv3 model
		self.net = cv.dnn.readNetFromDarknet(config_path, weight_path)

		# Get the output layer names of the model
		self.layer_names = self.net.getLayerNames()
		self.layer_names = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]


	def detect_object(self, image_path, imgPathResult):

		# FLAGS.image_path = "image_receive/laptop.jpg"
		# Do inference with given image
		# Intializing colors to represent each label uniquely
		colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype='uint8')

		# Read the image
		try:
			img = cv.imread(image_path)
			height, width = img.shape[:2]
		except:
			raise 'Image cannot be loaded!\n\
								Please check the path provided!'

		finally:
			img, arr_labels, _, _, _, _ = infer_image(self.net, self.layer_names, height, width, img, colors, self.labels, self.showtime, self.confidence, self.threshold)
			# show_image(img)
			cv.imwrite(imgPathResult,img)
			return img, arr_labels
