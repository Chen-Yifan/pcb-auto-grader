import numpy as np
from matplotlib import pyplot as plt
from time import time
import os
import cv2
from skimage import color


############################################### file loading related methods ###############################################

def load_img(path):
    """
    load image from path
    path: input path of image
    """
    return cv2.imread(path)

def get_all_top_image_paths(root='../data/processed_data/'):
    return [root+x for x in os.listdir(root) if 'top' in x and 'copper' not in x]

def get_all_copper_image_paths(root='../data/processed_data/'):
    return [root+x for x in os.listdir(root) if 'top' in x and 'copper' in x]




############################################### component related methods ###############################################

def load_components():
    """ 
    return: dict containing 5 components
    """
    power_supply = np.load('./data/components/power_supply.npy')
    capacitance = np.load('./data/components/capacitance.npy')
    LED = np.load('./data/components/LED.npy')
    resistance = np.load('./data/components/resistance.npy')
    regulation = np.load('./data/components/regulation.npy')
    return {
        'power_supply':power_supply,
        'capacitance': capacitance,
        'LED': LED,
        'resistance': resistance,
        'regulation': regulation,
    }


def get_all_rotated_components(comp):
    """
    comp: input component
    return: all rotations (90 deg) of this component
    """
    res = []
    for i in range(4):
        res.append(comp)
        comp = np.rot90(comp)
    return res




############################################### preprocessing related methods ###############################################


def get_gray_norm_image(img):
    """
    get the grayscale normalized image 
    img: the image represented in numpy format
    """    
    gray_img = color.rgb2gray(img)
    norm_img = gray_img/255.
    return norm_img


def get_threshold_gray_img(img):
    """
    get the thresholded image by OTSU's method 
    img: the image represented in numpy format
    return: the threshold image by OTSU
    """
    assert img is not None
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) 
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU) 
    return thresh


def crop(img):
    """
    Crop the empty starting and ending rows and cols to reduce search space
    img: the image represented in numpy format
    return: (the cropped image, left upper corner position)
    """
    start_row, start_col, end_row, end_col = 0, 0, len(img)-1, len(img[0])-1
    while np.sum(img[start_row]) == 0:
        start_row += 1
        if start_row == len(img):
            return None, [0, 0]
    while np.sum(img[:, start_col]) == 0:
        start_col += 1
    while np.sum(img[end_row]) == 0:
        end_row -= 1
    while np.sum(img[:, end_col]) == 0:
        end_col -= 1
    return img[start_row:end_row+1, start_col:end_col+1], [start_row, start_col]



def check_erosion(img, iterations=6):
    """
    erode the image for iterations
    img: the image represented in numpy format
    iteration: number of iterations to erodd
    """
    kernel = np.ones((5,5))
    erosion = cv2.erode(img,kernel,iterations = iterations)
    return erosion




############################################### other helper methods ###############################################


def get_next_boundary_component(img, debug=False, tol=6):
    """
    get the next connected component in img (assume input image is cropped)
    img: the image represented in numpy format
    tol: maximum distance of a neighbor 
    return: the bounding box for the predicted component
    """
    m, n = img.shape
    visited = set()
    all_boundary_ixs = []
    all_boundary_ixs += [(i, 0) for i in range(m)]
    all_boundary_ixs += [(i, n-1) for i in range(m)]
    all_boundary_ixs += [(0, j) for j in range(n)]
    all_boundary_ixs += [(m-1, j) for j in range(n)]
    start_ix = next(ix for ix in all_boundary_ixs if img[ix[0], ix[1]] > 0)
    
    
    queue = []
    queue.append(start_ix)
    visited.add(start_ix)
    while queue:
        i, j = queue.pop()
        for ni in range(i-tol, i+tol+1):
            for nj in range(j-tol, j+tol+1): # squared search (as effective as linear)
                if ni < 0 or nj < 0 or ni >= m or nj >= n:
                    continue
                if (ni, nj) in visited or img[ni, nj] == 0:
                    continue
                visited.add((ni, nj))
                queue.append((ni, nj))
    
    
    start_row = min(x[0] for x in visited)
    end_row = max(x[0] for x in visited)
    start_col = min(x[1] for x in visited)
    end_col = max(x[1] for x in visited)
    if debug:
        plt.figure()
        plt.imshow(img[start_row:end_row+1, start_col:end_col+1], cmap='gray')
        
    res = np.array(img[start_row:end_row+1, start_col:end_col+1])
    img[start_row:end_row+1, start_col:end_col+1] = 0
    return start_row, start_col, end_row, end_col 


def get_similarity(comp, mask):
    """
    Get similarity score (0-1) of component with mask of different shapes
    """
    resized_mask = cv2.resize(mask, comp.T.shape)
    assert(resized_mask.shape == comp.shape)
    return np.sum(comp==resized_mask) / comp.shape[0] / comp.shape[1]



############################################### main detection methods ###############################################


def detect_component_thresh(img, component, similarity_tol = 0.9):
    """
    Detect all rotations of a component from the image
    Inefficent implementation. The more efficient is to first get all components then try each
    img;  the image represented in numpy format
    component: target component
    similarity_tol: tolerance of similarity score to be accepted as first detected component
    return: best bounding box for component, None if not detected
    """
    cum_offsets = [0, 0]
    thresh = get_threshold_gray_img(img)
    cropped_img, offsets = crop(np.array(thresh))
    cum_offsets[0] += offsets[0]
    cum_offsets[1] += offsets[1]
    while cropped_img is not None:
        start_row, start_col, end_row, end_col  = get_next_boundary_component(cropped_img)
        start_row += cum_offsets[0]
        end_row += cum_offsets[0]
        start_col += cum_offsets[1]
        end_col += cum_offsets[1]

        for rot_comp in get_all_rotated_components(component):
            if get_similarity(thresh[start_row:end_row+1, start_col:end_col+1], rot_comp) >= similarity_tol:
                return start_row, start_col, end_row,  end_col

        cropped_img, offsets = crop(cropped_img)
        cum_offsets[0] += offsets[0]
        cum_offsets[1] += offsets[1]
    return None 


def detect_component_sliding_window(img, component):
    """
    img;  the image represented in numpy format
    component: target component
    return: best bounding box for component, None if not detected
    """
    start_time = time()
    img = get_gray_norm_image(img)
    best_score, best_res  = -1, None
    rot_components = get_all_rotated_components(component)
    for component in rot_components:
        med = np.median(img)
        signed_img = np.where(img > med, 1, -1)
        signed_component = np.where(component > med, 1, -1)
        m1, n1 = signed_img.shape[:2]
        m2, n2 = signed_component.shape[:2]
        convolved = np.zeros(signed_img.shape)
        for i in range(m1-m2):
            for j in range(n1-n2):
                convolved[i, j] = np.sum(signed_img[i:i+m2, j:j+n2]*signed_component)
        loc = np.argmax(convolved.ravel())
        i, j = loc//n1, loc % n1
        matched = np.zeros(img.shape)
        matched[i:i+m2, j:j+n2] = img[i:i+m2, j:j+n2]
        if (convolved.ravel()[loc] > best_score):
            best_score = convolved.ravel()[loc]
            best_res =  i, j, i+m2, j+n2 
            
    print('detection (sliding window): {} seconds elapsed'.format(time()-start_time))
    return best_res 



############################################### plot assisted functions ###############################################
def get_bounding_box_from_img(img, bounding_box):
    """
    img: the image represented in numpy format
    bounding_box: tuple representing bounding box
    return: subarray of the represented bounding box
    """
    start_row, start_col, end_row, end_col = bounding_box
    return img[start_row:end_row+1, start_col:end_col+1]

def compare_img(original, predicted, orig_title='original', pred_title='predicted'):
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(original)
    plt.title(orig_title)
    
    plt.subplot(1, 2, 2)
    plt.imshow(predicted)
    plt.title(pred_title)