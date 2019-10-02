import numpy as np
import argparse
import cv2 as cv
import subprocess
import time
import os
from core.string_resource import StringResource
from PIL import ImageFont, ImageDraw, Image
import random

def show_image(img):
    cv.imshow("Image", img)
    cv.waitKey(0)

def draw_labels_and_boxes(img, boxes, confidences, classids, idxs, colors, labels):
    # If there are any detections
    arr_label= []
    if len(idxs) > 0:
        for i in idxs.flatten():
            # Get the bounding box coordinates
            x, y = boxes[i][0], boxes[i][1]
            w, h = boxes[i][2], boxes[i][3]
            
            # Get the unique color for this class
            color = [int(c) for c in colors[classids[i]]]

            # Draw the bounding box rectangle and label on the image
            cv.rectangle(img, (x, y), (x+w, y+h), color, 5)

            label_name = StringResource.OBJECT_NAME_JA.get(labels[classids[i]].replace(" ", "_").lower())
            # text = "{}: {:4f}".format(labels[classids[i]], confidences[i])
            text = "{}: {:4f}".format(label_name, confidences[i])
            

            x = 10 if x < 5 else x
            y = (y + h) if (y-5) < 0 else (y-5)

            fontpath ='./font/hgrpp1.ttc'
            font = ImageFont.truetype(fontpath, 50)

            # cv.putText(img, text, (x, y-5), cv.FONT_HERSHEY_SIMPLEX, 1.5, color, 4)
            # cv.putText(img, text, (x, y-5), font, 1.5, color, 4)

            img_pil = Image.fromarray(img)
            draw = ImageDraw.Draw(img_pil)
            
            draw.text((x, y+10),  text, font = font, fill = StringResource.TEXT_CORLOR[random.randrange(len(StringResource.TEXT_CORLOR)-1)])

            img = np.array(img_pil)

            if label_name not in arr_label:
                # label_name = labels[classids[i]].replace(" ", "_").lower()
                arr_label.append(label_name)

    return img, arr_label


def generate_boxes_confidences_classids(outs, height, width, tconf):
    boxes = []
    confidences = []
    classids = []

    for out in outs:
        for detection in out:
            #print (detection)
            #a = input('GO!')
            
            # Get the scores, classid, and the confidence of the prediction
            scores = detection[5:]
            classid = np.argmax(scores)
            confidence = scores[classid]
            
            # Consider only the predictions that are above a certain confidence level
            if confidence > tconf:
                # TODO Check detection
                box = detection[0:4] * np.array([width, height, width, height])
                centerX, centerY, bwidth, bheight = box.astype('int')

                # Using the center x, y coordinates to derive the top
                # and the left corner of the bounding box
                x = int(centerX - (bwidth / 2))
                y = int(centerY - (bheight / 2))

                # Append to list
                boxes.append([x, y, int(bwidth), int(bheight)])
                confidences.append(float(confidence))
                classids.append(classid)

    return boxes, confidences, classids

def infer_image(net, layer_names, height, width, img, colors, labels, show_time, confidence, threshold,
            boxes=None, confidences=None, classids=None, idxs=None, infer=True):
    
    if infer:
        # Contructing a blob from the input image
        blob = cv.dnn.blobFromImage(img, 1 / 255.0, (416, 416), 
                        swapRB=True, crop=False)

        # Perform a forward pass of the YOLO object detector
        net.setInput(blob)

        # Getting the outputs from the output layers
        start = time.time()
        outs = net.forward(layer_names)
        end = time.time()

        if show_time:
            print ("[INFO] YOLOv3 took {:6f} seconds".format(end - start))

        
        # Generate the boxes, confidences, and classIDs
        boxes, confidences, classids = generate_boxes_confidences_classids(outs, height, width, confidence)
        
        # Apply Non-Maxima Suppression to suppress overlapping bounding boxes
        idxs = cv.dnn.NMSBoxes(boxes, confidences, confidence, threshold)

    if boxes is None or confidences is None or idxs is None or classids is None:
        raise '[ERROR] Required variables are set to None before drawing boxes on images.'
        
    # Draw labels and boxes on the image
    img, arr_labels = draw_labels_and_boxes(img, boxes, confidences, classids, idxs, colors, labels)

    return img, arr_labels, boxes, confidences, classids, idxs