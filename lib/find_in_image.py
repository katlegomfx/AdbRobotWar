import cv2
import cv2 as cv
from PIL import Image as im 
import numpy as np
from matplotlib import pyplot as plt


def finding(real, get, render=False):

    # img_rgb = cv2.imread(real)
    # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(get,0)
    w, h = template.shape[::-1]

    res = cv2.matchTemplate(cv2.cvtColor(real, cv2.COLOR_BGR2GRAY),template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where( res >= threshold)
    average_x = []
    average_y = []
    for pt in zip(*loc[::-1]):
        cv2.rectangle(real, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
        average_x.append(pt[0])
        average_y.append(pt[1])

    x_difs = [j-i for i, j in zip(average_x[1:], average_x)] 
    y_difs = [j-i for i, j in zip(average_y[1:], average_y)] 
    # print(x_difs, y_difs)
    
    x_difs = [x for x in x_difs if -5 <= x <= 5] 
    y_difs = [y for y in y_difs if -5 <= y <= 5] 
    # print(x_difs, y_difs)

    if render:
        plt.imshow(real)
        plt.show()

    if len(x_difs) > 3 and len(y_difs) > 3:
        final_x = sum(average_x)/len(average_x) + w/2
        final_y = sum(average_y)/len(average_y) + h/2
        return final_x, final_y
    else:
        return None

if __name__=='__main__':
    print(finding())