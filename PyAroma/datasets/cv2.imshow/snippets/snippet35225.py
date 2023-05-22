import base64
import datetime
import io
import json
import os
import time
import webbrowser
import colorama
import cv2
import numpy
from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtCore import Qt, QByteArray
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtWidgets import QFileDialog
from keras.models import model_from_json

if (__name__ == '__main__'):
    if (os.name == 'nt'):
        os.system('cls')
    else:
        os.system('clear')
    colorama.init(autoreset=True)
    imdir = None
    print(APP_INFO)
    print((colorama.Fore.LIGHTBLACK_EX + '[DEBUG] Loading application... '), end='')
    if RUN_FLAG:
        print((colorama.Fore.LIGHTGREEN_EX + 'done'))
    else:
        print((colorama.Fore.LIGHTRED_EX + 'integrity failure'))
    while RUN_FLAG:
        image = launcher(imdir)
        if (image is None):
            print((colorama.Fore.LIGHTBLACK_EX + '[DEBUG] Exiting application...'))
            break
        elif (not os.path.isfile(image)):
            print((colorama.Fore.LIGHTRED_EX + '[ERROR] File does not exist'))
            continue
        try:
            image_orig = cv2.imread(image, cv2.IMREAD_COLOR)
        except:
            image_orig = None
        if (image_orig is None):
            print((colorama.Fore.LIGHTRED_EX + '[ERROR] Failed to read image'))
            continue
        else:
            print((colorama.Fore.LIGHTGREEN_EX + f'[DEBUG] Loaded new image from: {image}'))
            imdir = os.path.dirname(image)
        cv2.namedWindow('STEFANN')
        grid = False
        fscale = 1.0
        points = []
        thresh = 150
        invert = 0
        cntmin = 0
        cntidx = 0
        edited = False
        step = 1
        cv2.setMouseCallback('STEFANN', select_region, points)
        image_scaled = image_orig.copy()
        while (step == 1):
            key = (cv2.waitKey(1) & 255)
            if (key == 27):
                print((colorama.Fore.LIGHTRED_EX + '[DEBUG] Operation canceled'))
                break
            elif ((key == 71) or (key == 103)):
                grid = (not grid)
                print((colorama.Fore.LIGHTCYAN_EX + f'[DEBUG] Toggled grids -> {grid}'))
            elif ((key == 82) or (key == 114)):
                fscale = 1.0
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Updated scale -> {fscale}x'))
                image_scaled = image_orig.copy()
                points.clear()
            elif (key == 43):
                fscale = round(min((fscale + DELTA_FSCALE), 5.0), 1)
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Updated scale -> {fscale}x'))
                image_scaled = cv2.resize(image_orig, None, fx=fscale, fy=fscale)
                points.clear()
            elif (key == 45):
                fscale = round(max((fscale - DELTA_FSCALE), 0.2), 1)
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Updated scale -> {fscale}x'))
                image_scaled = cv2.resize(image_orig, None, fx=fscale, fy=fscale)
                points.clear()
            elif (key == 13):
                step += 1
            image_work = (draw_grid(image_scaled) if grid else image_scaled.copy())
            image_work = draw_region(image_work, points)
            cv2.imshow('STEFANN', image_work)
        cv2.setMouseCallback('STEFANN', select_region, None)
        image_edit = image_scaled.copy()
        image_gray = cv2.cvtColor(image_scaled, cv2.COLOR_BGR2GRAY)
        image_mask = binarize(image_gray, points, thresh, 255, invert)
        (contours, bndboxes) = find_contours(image_mask, cntmin)
        while (step == 2):
            key = (cv2.waitKey(1) & 255)
            if (key == 27):
                print((colorama.Fore.LIGHTRED_EX + '[DEBUG] Operation canceled'))
                break
            elif (key == 43):
                thresh = min((thresh + DELTA_THRESH), 255)
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Increased threshold -> {thresh}'))
                image_mask = binarize(image_gray, points, thresh, 255, invert)
                (contours, bndboxes) = find_contours(image_mask, cntmin)
            elif (key == 45):
                thresh = max((thresh - DELTA_THRESH), 0)
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Decreased threshold -> {thresh}'))
                image_mask = binarize(image_gray, points, thresh, 255, invert)
                (contours, bndboxes) = find_contours(image_mask, cntmin)
            elif (key == 9):
                invert = int((not invert))
                print((colorama.Fore.LIGHTCYAN_EX + f'[DEBUG] Invert thresholding -> {invert}'))
                image_mask = binarize(image_gray, points, thresh, 255, invert)
                (contours, bndboxes) = find_contours(image_mask, cntmin)
            elif (key == 42):
                cntmin = min((cntmin + DELTA_CNTMIN), (image_mask.shape[0] * image_mask.shape[1]))
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Increased allowed contour area -> {cntmin}'))
                (contours, bndboxes) = find_contours(image_mask, cntmin)
            elif (key == 47):
                cntmin = max((cntmin - DELTA_CNTMIN), 0)
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Decreased allowed contour area -> {cntmin}'))
                (contours, bndboxes) = find_contours(image_mask, cntmin)
            elif (key == 32):
                cntidx = (((cntidx + 1) % len(contours)) if (len(contours) > 0) else (- 1))
            elif (((key >= 65) and (key <= 90)) or ((key >= 97) and (key <= 122))):
                if ((key >= 97) and (key <= 122)):
                    key -= 32
                print((colorama.Fore.CYAN + f'[DEBUG] Inserting character -> {chr(key)}'))
                try:
                    (image_mask, image_edit) = edit_char(image_edit, image_mask, contours, bndboxes, cntidx, chr(key), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', NET_F, NET_C)
                except:
                    print((colorama.Fore.LIGHTRED_EX + '[ERROR] Operation failed'))
                    continue
                image_gray = cv2.cvtColor(image_edit, cv2.COLOR_BGR2GRAY)
                (contours, bndboxes) = find_contours(image_mask, cntmin)
                edited = True
            elif (key == 8):
                print((colorama.Fore.LIGHTRED_EX + '[DEBUG] Reset modifications'))
                image_edit = image_scaled.copy()
                image_gray = cv2.cvtColor(image_scaled, cv2.COLOR_BGR2GRAY)
                image_mask = binarize(image_gray, points, thresh, 255, invert)
                (contours, bndboxes) = find_contours(image_mask, cntmin)
                edited = False
            elif (key == 13):
                step += 1
            image_work = draw_contours(image_mask, contours, cntidx, (0, 255, 0), cv2.COLOR_GRAY2BGR)
            cv2.imshow('STEFANN', image_work)
        if edited:
            image_edit = watermark(image_edit, 'Edited with STEFANN', alpha=0.3, position=3)
            (root, ext) = os.path.splitext(image)
            file_path = (((root + '_') + timestamp()) + ext)
            try:
                cv2.imwrite(file_path, image_edit)
                print((colorama.Fore.LIGHTGREEN_EX + f'[DEBUG] Edited image saved as: {file_path}'))
            except:
                print((colorama.Fore.LIGHTRED_EX + '[ERROR] Failed to write image'))
        change = False
        layout = 0
        labels = False
        fscale = 1.0
        image_work = image_edit.copy()
        while (step == 3):
            key = (cv2.waitKey(1) & 255)
            if ((key == 13) or (key == 27)):
                break
            elif (key == 32):
                layout = ((layout + 1) % 6)
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Select layout -> {layout}'))
                change = True
            elif (key == 9):
                labels = (not labels)
                print((colorama.Fore.LIGHTCYAN_EX + f'[DEBUG] Toggled label -> {labels}'))
                change = True
            elif (key == 43):
                fscale = round(min((fscale + DELTA_FSCALE), 2.5), 1)
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Updated scale -> {fscale}x'))
                change = True
            elif (key == 45):
                fscale = round(max((fscale - DELTA_FSCALE), 0.2), 1)
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Updated scale -> {fscale}x'))
                change = True
            elif ((key == 82) or (key == 114)):
                fscale = 1.0
                print((colorama.Fore.LIGHTBLACK_EX + f'[DEBUG] Updated scale -> {fscale}x'))
                change = True
            elif ((key == 83) or (key == 115)):
                (root, ext) = os.path.splitext(image)
                file_path = (((root + '_') + timestamp()) + ext)
                try:
                    cv2.imwrite(file_path, image_work)
                    print((colorama.Fore.LIGHTGREEN_EX + f'[DEBUG] Image layout saved as: {file_path}'))
                except:
                    print((colorama.Fore.LIGHTRED_EX + '[ERROR] Failed to write image'))
            if change:
                image_work_0 = cv2.resize(image_scaled, None, fx=fscale, fy=fscale)
                image_work_1 = cv2.resize(image_edit, None, fx=fscale, fy=fscale)
                (rows, cols) = image_work_0.shape[:2]
                h_bar_1 = numpy.zeros((10, cols, 3), numpy.uint8)
                v_bar_1 = numpy.zeros((rows, 10, 3), numpy.uint8)
                if labels:
                    image_work_0 = watermark(image_work_0, 'ORIGINAL', 20, color=(255, 255, 0), alpha=0.7, position=4)
                    image_work_1 = watermark(image_work_1, 'EDITED', 20, color=(0, 255, 0), alpha=0.7, position=4)
                if (layout == 0):
                    image_work = image_work_1.copy()
                elif (layout == 1):
                    image_work = image_work_0.copy()
                elif (layout == 2):
                    image_work = numpy.hstack((image_work_0, v_bar_1, image_work_1))
                elif (layout == 3):
                    image_work = numpy.hstack((image_work_1, v_bar_1, image_work_0))
                elif (layout == 4):
                    image_work = numpy.vstack((image_work_0, h_bar_1, image_work_1))
                elif (layout == 5):
                    image_work = numpy.vstack((image_work_1, h_bar_1, image_work_0))
                change = False
            cv2.imshow('STEFANN', image_work)
        cv2.destroyAllWindows()
    colorama.deinit()
    time.sleep(2)
