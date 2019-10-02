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

		# label_path= "./model/clock-glass-laptop"
		# config_path = "./model/clock_glass_laptop.cfg"
		# weight_path = "./model/clock_glass_laptop_5000.weights"

		# label_path= "./model/Clock_Glass_Laptop_20190919161459252795"
		# config_path = "./model/Clock_Glass_Laptop_20190919161459252795.cfg"
		# weight_path = "./model/Clock_Glass_Laptop_20190919161459252795_6000.weights"


		self.pathConfig = [
			{
				"label_path": "./model/Clock_Glass_Laptop_20190919161459252795",
				"config_path": "./model/Clock_Glass_Laptop_20190919161459252795.cfg",
				"weight_path": "./model/Clock_Glass_Laptop_20190919161459252795_6000.weights"
			},
			{
				"label_path": "./model/coco-labels",
				"config_path": "./model/yolov3.cfg",
				"weight_path": "./model/yolov3.weights"
			}
			

		]

		self.confidence = 0.5
		self.threshold = 0.3
		self.showtime = False

		# Get the labels
		self.labels = []
		self.layer_names = []
		# Load the weights and configutation to form the pretrained YOLOv3 model
		self.nets = []
		for i in range(0, len(self.pathConfig)):
			net = cv.dnn.readNetFromDarknet(self.pathConfig[i].get("config_path"), self.pathConfig[i].get("weight_path"))
			self.nets.append(net)
			self.labels.append(open(self.pathConfig[i].get("label_path")).read().strip().split('\n'))

			# Get the output layer names of the model
			layer_names = net.getLayerNames()
			self.layer_names.append([layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()])
		


	def detect_object(self, image_path, imgPathResult, model=1):

		# FLAGS.image_path = "image_receive/laptop.jpg"
		# Do inference with given image
		# Intializing colors to represent each label uniquely
		colors = np.random.randint(0, 255, size=(len(self.labels[model]), 3), dtype='uint8')

		# Read the image
		try:
			img = cv.imread(image_path)
			height, width = img.shape[:2]
		except:
			raise 'Image cannot be loaded!\n\
								Please check the path provided!'

		finally:
			img, arr_labels, _, _, _, _ = infer_image(self.nets[model], self.layer_names[model], height, width, img, colors, self.labels[model], self.showtime, self.confidence, self.threshold)
			# show_image(img)
			cv.imwrite(imgPathResult,img)
			return img, arr_labels
