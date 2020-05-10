import numpy as np
import collections
import cv2
import os

def grade_trace(basedir, labels, boxes):
    top_copper_image = cv2.imread(os.path.join(basedir, "top-copper.png"))

    bounding_boxes = []
    for i in range(len(labels)):
        bounding_boxes.append((boxes[i], labels[i]))

    graph = get_topology(top_copper_image, bounding_boxes)

    score = 0
    explanation = ""

    # Grade topology
    for component in graph:
        if component == "power_supply":
            if "regulation" in graph[component]:
                score += 1
                explanation += "Correct +1! Power_supply and regulator are connected\n"
            if "resistance" in graph[component]:
                explanation += "Incorrect! Power supply should not directly connect to resistor"
        if component == "resistance":
            if "regulation" in graph[component]:
                score += 1
                explanation += "Correct +1! resistor and regulator are connected\n"
        if component == "capacitance":
            if "regulation" in graph[component]:
                score += 1
                explanation += "Correct +1! Capacitance and power_supply are connected\n"

    return score, explanation

def in_box(bounding_box, pos, tol=0):
    """
    tol: tolerance of bounding box boundary
    return: whether the position is inside the bounding box
    """

    return bounding_box[0] - tol <= pos[1] <= bounding_box[2] + tol and bounding_box[1] - tol <= pos[0] <= bounding_box[
        3] + tol  # coordinate space are swapped


def get_all_connected_pixels(img, start_pos):
    """
    Two pixels are called connected if there is a sequence of intermediate pixels that are exactly the same and are adjacent to each other
    return: all pixels connected to the start_pos.
    """

    queue = collections.deque()
    visited = set()
    pixel = img[start_pos[0]][start_pos[1]]
    queue.append(start_pos)
    visited.add(start_pos)

    while queue:
        pos = queue.popleft()
        for i, j in [[pos[0] - 1, pos[1]], [pos[0], pos[1] - 1], [pos[0] + 1, pos[1]], [pos[0], pos[1] + 1]]:
            if 0 <= i < len(img) and 0 <= j < len(img[0]) and (i, j) not in visited and img[i][j] == pixel:
                queue.append((i, j))
                visited.add((i, j))
    return visited

def area_coverage(img, points):
    """
    Calculate IOU with tightest bounding box
    """
    min_row = min(p[0] for p in points)
    min_col = min(p[1] for p in points)
    max_row = max(p[0] for p in points)
    max_col = max(p[1] for p in points)

    intersection = len(points)
    union = (max_row - min_row + 1) * (max_col - min_col + 1)
    return intersection / union

def to_binary_copper(img):
    """
    img: input copper img in numpy format
    return: binary image
    """
    return np.array(img[:, :, 0] > 0.5).astype('int')

def detect_traces(img):
    """
    img: input copper image in numpy format
    return: list of [points contained in each trace]
    """
    img = to_binary_copper(img)
    visited = set()
    res = []
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] == 1 and (i, j) not in visited:
                all_connected = get_all_connected_pixels(img, (i, j))
                if area_coverage(img, all_connected) < 0.3:
                    res.append(all_connected)
                visited = visited.union(all_connected)
    return res


def get_topology(copper_img, component_bbs, verbose=False):
    """
    copper_img: input copper img in numpy format
    component_bbs: loaded label file in bounding box format
    """
    graph = collections.defaultdict(set)
    for trace in detect_traces(copper_img):
        all_labels = set()
        for i, j in trace:
            for bounding_box, label in component_bbs:
                if in_box(bounding_box, (i, j)):
                    all_labels.add(label)

        for label_a in all_labels:
            for label_b in all_labels:
                if label_a != label_b:
                    graph[label_a].add(label_b)
                    graph[label_b].add(label_a)
    return graph