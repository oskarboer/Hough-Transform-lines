import cv2
from math import *
import numpy as np


def Hough_lines(img):
    # retval, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)

    height, width = img.shape[:2]
    accumulator = np.zeros((180, int(sqrt(height ** 2 + width ** 2))), dtype=np.int)

    # need to create 2d array so I can use np.vstack() later
    lines = np.array([[0, 0], [0, 0]])
    # line length in pixels
    line_length = 100

    # look for every pixel
    for y in range(0, height):
        for x in range(0, width):
            # if pixel is black (possible part of a line)
            if img[y][x] < 20:
                line = []
                # try all angles (if you need more precise just decrease step)
                for theta in range(0, 180):
                    p = int(x * cos(radians(theta)) + y * sin(radians(theta)))
                    accumulator[theta][p] += 1
                    # Check if it looks like line and if it's not in a list
                    if (accumulator[theta][p] > line_length) and (p not in lines[:, 0]) and (theta not in lines[:, 1]):
                        lines = np.vstack((lines, np.array([p, theta])))

    # clean two first zeros
    lines = np.delete(lines, [0, 1], axis=0)

    return lines

# find all intersection with borders of a image
def line_intersection(p, theta, img):
    h, w = img.shape[:2]
    out = []
    theta = radians(theta)
    intersect = [int(round(p / sin(theta))), int(round((p - w * cos(theta)) / sin(theta))), int(round(p / cos(theta))),
                 int(round((p - h * sin(theta)) / cos(theta)))]
    if (intersect[0] > 0) and (intersect[0] < h):
        out.append((0, intersect[0]))
    if (intersect[1] > 0) and (intersect[1] < h):
        out.append((w, intersect[1]))

    if (intersect[2] > 0) and (intersect[2] < w):
        out.append((intersect[2], 0))
    if (intersect[3] > 0) and (intersect[3] < w):
        out.append((intersect[3], h))
    return out


def main():
    img = cv2.imread("line_easy.png", 0)
    lines = Hough_lines(img)
    print(lines)

    for i in lines:
        points = line_intersection(i[0], i[1], img)
        print(points)
        cv2.line(img, points[0], points[1], [100])

    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
