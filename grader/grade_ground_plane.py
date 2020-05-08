import torch.nn as nn
import torch
from matplotlib.pyplot import imread
import cv2
import os
from torchvision.transforms import ToTensor

class GroundPlaneNet(nn.Module):
    def __init__(self):
        super(GroundPlaneNet, self).__init__()
        self.conv1 = nn.Conv2d(3, 1, 5, stride=2, dilation=2)
        self.fc1 = nn.Linear(116 * 116, 1)

    def forward(self, x):
        x = self.conv1(x)
        x = x.view(-1, 116 * 116)
        x = self.fc1(x)
        # x = torch.sigmoid(x)
        return x

def grade_ground_plane(basedir):
    ground_plane_count = 0

    model = GroundPlaneNet()
    model.load_state_dict(torch.load("GroundDetectionModel.pth"))
    model.eval()

    top_img = imread(os.path.join(basedir,"top-copper.png"))
    bottom_img = imread(os.path.join(basedir, "bottom-copper.png"))
    resized_top_img = ToTensor()(cv2.resize(top_img, dsize=(240, 240), interpolation=cv2.INTER_CUBIC))
    resized_bottom_img = ToTensor()(cv2.resize(bottom_img, dsize=(240, 240), interpolation=cv2.INTER_CUBIC))

    output_top = model(resized_top_img.unsqueeze(0))
    output_bottom = model(resized_bottom_img.unsqueeze(0))

    ground_plane_count += 1 if output_top.data.cpu().numpy()[0, 0] > 0 else 0
    ground_plane_count += 1 if output_bottom.data.cpu().numpy()[0, 0] > 0 else 0

    score = 1 if ground_plane_count > 0 else 0
    explanation = "ground_plane_found" if ground_plane_count > 0 else "ground_plane_notfound"
    return score, explanation