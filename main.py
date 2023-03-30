import random
import imutils
import numpy as np
import cv2
import argparse

def make_data(path, level, limit) :
    blur = 21
    dilate_iter = 10


    img = cv2.imread(path)

    test = img.copy()
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    thresh = cv2.Canny(imgray, 150, 200)
    thresh = cv2.dilate(thresh, None)
    thresh = cv2.erode(thresh, None)
    kernel_c = np.ones((5,5),np.uint8)
    kernel_o = np.ones((1,1),np.uint8)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel_c)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel_o)
    contour_info = [(c, cv2.contourArea(c)) for c in cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]]
    print('Number of contours =  ' + str(len(contour_info)))

    area = set([contour[1] for contour in contour_info])
    area = sorted(area)
    print('List area: ' + str(area))
    lenght = len(area)
    Lv3_min = area[0]
    Lv3_max = area[int(lenght / 2)]
    Lv2_min = area[int(lenght / 2) + 1]
    Lv2_max = area[int(lenght / 2) + int(lenght / 3)]
    Lv1_min = area[int(lenght / 2) + int(lenght / 3) + 1]
    Lv1_max = area[lenght - 1]

    if level == 1:
        minn = Lv1_min
        maxx = Lv1_max
    elif level == 2:
        minn = Lv2_min
        maxx = Lv2_max
    elif level == 3:
        minn = Lv3_min
        maxx = Lv3_max
    minn = max(minn, 100)
    maxx = min(maxx, 30000)
    Limit = limit
    print("Min - Max: " + str(minn) + " " + str(maxx))
    print("Limit: " + str(Limit))

    def myFunc(e):
        return e[1]

    contour_info.sort(reverse=True, key=myFunc)
    for contour in contour_info:
        area = contour[1]
        al = np.random.randint(1, 100)
        if area >= minn and area <= maxx and al % 3 == 0:
            x, y, w, h = cv2.boundingRect(contour[0])
            color = img[y + h // 2, x + w // 2]
            new_color = (np.random.uniform(0, 255), np.random.uniform(0, 255), np.random.uniform(0, 255));
            cv2.fillPoly(img, [contour[0]], new_color)
            Limit = Limit - 1
            # cv2.drawContours(img, [contour[0]], 0, (0, 0, 255), 3)
            if (Limit == 0):
                break

    cv2.imwrite('export/Check.jpg', thresh)
    cv2.imwrite('export/Left.jpg', test)
    cv2.imwrite('export/Right.jpg', img)

    return test, img

def find_the_differences(test, img):

    img1 = test
    img2 = img

    img1 = imutils.resize(img1, height=1200)
    img2 = imutils.resize(img2, height=1200)

    img_height = img1.shape[0]

    diff = cv2.absdiff(img1, img2)

    diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

    for i in range(0, 3):
        dilated = cv2.dilate(diff.copy(), None, iterations=i + 1)
    (T, thresh) = cv2.threshold(dilated, 3, 255, cv2.THRESH_BINARY)

    kernel = np.ones((3,3), np.uint8)
    dilate = cv2.dilate(thresh, kernel, iterations=5)
    cv2.imshow("Dilate", dilate)

    contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    count = 0
    for contour in contours:
        if cv2.contourArea(contour) >= 60:
            count = count + 1
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)

    x = np.zeros((img_height,10,3), np.uint8)
    result = np.hstack((img1, x, img2))
    print("Number of differences:", str(count))
    cv2.imshow("Differences", result)
    cv2.imwrite('export/result.jpg', result)


    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='The script will spot the differences between two images, circle and number them. ')
    my_parser.add_argument('--img', action='store', type=str, help='the path to image', default='ImageIN/Test.jpg')
    my_parser.add_argument('--level', action='store', type=int, help='level game', default=1)
    my_parser.add_argument('--limit', action='store', type=int, help='limit difference', default=5)
    # python3 main.py --img 'ImageIN/doraemon1.jpg' --level 2 --limit 10


    # IMG1 = input('Enter path to image 1: ')
    # IMG2 = input('Enter path to image 2: ')
    args = my_parser.parse_args()
    IMG = args.img
    Level = args.level
    Limit = args.limit

    left, right = make_data(IMG, Level, Limit)
    find_the_differences(left, right)