#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import numpy as np

def biggest_contour(contours):
    biggest = np.array([])
    max_area = 0
    
    for contour in contours:

        area = cv2.contourArea(contour)
        
        if area > 1000:

            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
                
    return biggest


def find_paper(image):

    '''
    Find an answer sheet in the image and auto crop it
    '''
    
    # define readed answersheet image output size
    (max_width, max_height) = (1000, 1300)
    
    img_original = image.copy()
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 10, 75, 75)  # Add bilateral filtering to reduce noise
    edged = cv2.Canny(gray, 10, 20)

    (contours, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    biggest = biggest_contour(contours)

    cv2.drawContours(image, [biggest], -1, (0, 255, 0), 3)

    # Pixel values in the original image
    points = biggest.reshape(4, 2)
    input_points = np.zeros((4, 2), dtype="float32")

    points_sum = points.sum(axis=1)
    input_points[0] = points[np.argmin(points_sum)]
    input_points[3] = points[np.argmax(points_sum)]

    points_diff = np.diff(points, axis=1)
    input_points[1] = points[np.argmin(points_diff)]
    input_points[2] = points[np.argmax(points_diff)]

    # Desired points values in the output image
    converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])

    # Perspective transformation
    matrix = cv2.getPerspectiveTransform(input_points, converted_points)
    img_output = cv2.warpPerspective(img_original, matrix, (max_width, max_height))
    
    return img_output


def read_answer(roi, debug=True):
    '''
    Read answer marks from a specific region of the answer sheet and return the results as a list.
    '''
    n_questions = 10
    
    grey = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grey, (3, 3), 0)  # Apply Gaussian blur to reduce noise
    (_, res) = cv2.threshold(blurred, 185, 255, cv2.THRESH_BINARY)

    res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=3)
    res = cv2.dilate(res, (3, 3), iterations=1)

    if debug:
        pass
#         cv2.imshow("Thresholded", res)
#         cv2.waitKey(0)

    (contours, _) = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    readed = []
    for cnt in contours[1:][::-1]:
        (x, y, w, h) = cv2.boundingRect(cnt)
        if w > 10 and h > 10:  # Filter out small contours
            if x in range(0, 32):
                readed.append((int(y // 80) + 1, 1))
            elif x in range(34, 67):
                readed.append((int(y // 80) + 1, 2))
            elif x in range(68, 99):
                readed.append((int(y // 80) + 1, 3))
            elif x in range(100, 132):
                readed.append((int(y // 80) + 1, 4))
    
    idx1=0
    for t1 in readed:
        for t2 in readed:
            if t1[0] == t2[0] and t1 != t2:
                x = (t1[0],None)
                readed.append(x)
                readed.pop(idx1)
        idx1+=1
    readed=set(readed)
    read = [None] * n_questions
    
    for (n, choice) in readed:
        read[n - 1] = choice
    
    return read




def id_read(image, debug=True):
    '''
    Read the ID from the ID section of the answer sheet image
    '''
    img = image
    
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grey, (3, 3), 0)  # Apply Gaussian blur to reduce noise
    (_, res) = cv2.threshold(blurred, 178, 255, cv2.THRESH_BINARY)

    res = cv2.morphologyEx(res, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8), iterations=4)
    res = cv2.dilate(res, (5, 5), iterations=3)

    Id = []
    (contours, _) = cv2.findContours(res, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
    for cnt in contours[1:][::-1]:
        (x, y, w, h) = cv2.boundingRect(cnt)
        if w > 10 and h > 10:  # Filter out small contours
            if y in range(0, 26):
                Id.append(0)
            elif y in range(26, 52):
                Id.append(1)
            elif y in range(52, 78):
                Id.append(2)
            elif y in range(78, 104):
                Id.append(3)
            elif y in range(104, 130):
                Id.append(4)
            elif y in range(130, 156):
                Id.append(5)
            elif y in range(156, 182):
                Id.append(6)
            elif y in range(182, 208):
                Id.append(7)
            elif y in range(208, 234):
                Id.append(8)
            elif y in range(234, 260):
                Id.append(9)
    
    return Id


