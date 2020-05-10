from detecto.core import Model, Dataset
from detecto import utils, visualize
import numpy as np
import os
import shutil
import torch


model_file = 'ComponentDetectionModel.pth'

device = 'cuda' if torch.cuda.is_available() else 'cpu'
#Faster R-CNN ResNet-50 FPN
model = torch.load(model_file, map_location=torch.device(device))
model._model = model._model.to(device)
model._device = device


def iou(boxA, boxB):
  interWidth = min(boxA[2], boxB[2])-max(boxA[0], boxB[0])+1
  interHeight = min(boxA[3], boxB[3])-max(boxA[1], boxB[1])+1
  interArea = max(interWidth, 0) * max(interHeight, 0)

  areaA = (boxA[2]-boxA[0]+1)*(boxA[3]-boxA[1]+1)
  areaB = (boxB[2]-boxB[0]+1)*(boxB[3]-boxB[1]+1)
  return interArea/(areaA+areaB-interArea)

def get_best_bounding_boxes(labels, boxes, scores):
  assert len(labels) == len(boxes) == len(scores)

  removeIx = set()
  for i in range(len(boxes)):
    for j in range(i+1, len(boxes)):
      if iou(boxes[i], boxes[j]).item() > 0.3:
        if scores[i] > scores[j]:
          removeIx.add(j)
        else:
          removeIx.add(i)

  remain_ixs = [i for i in range(len(boxes)) if i not in removeIx]
  labels = [labels[i] for i in range(len(boxes)) if i not in removeIx]
  boxes = boxes[remain_ixs]
  scores = scores[remain_ixs]
  return labels, boxes, scores

def grade_components(basedir):
  filename = os.path.join(basedir, "top.png")
  image = utils.read_image(filename)
  labels, boxes, scores = model.predict(image)
  labels, boxes, scores = get_best_bounding_boxes(labels, boxes, scores)
  boxes = boxes.data.detach().numpy()

  explanation = ""

  score_dict = dict(regulation=0,capacitance=0,resistance=0,LED=0,power_supply=0)

  for idx in range(len(labels)):
    score_dict[labels[idx]] = 1
    explanation += "{} detected at {} with confidence {}\n".format(labels[idx], boxes[idx], scores[idx])

  score = sum(score_dict.values())

  for label in score_dict:
    if score_dict[label] == 0:
      explanation += "{} not detected\n".format(label)

  return score, explanation, labels, boxes, scores