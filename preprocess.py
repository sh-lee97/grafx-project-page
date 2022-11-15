from glob import glob
import os; opj = os.path.join
import numpy as np
from PIL import Image
from tqdm import tqdm
import cv2

pdf_dirs = glob('samples/*/*/*/autoencoding.pdf')
for pdf_dir in tqdm(pdf_dirs):
    split = pdf_dir.split('/')
    png_dir = '/'.join(split[:-1]+[split[-1].split('.')[0]+'.png'])
    os.system(f'pdftoppm {pdf_dir} {png_dir} -png -f 1 -l 2 -rx 500 -ry 500')

png_dirs = glob('samples/*/*/*/*.png')
for png_dir in tqdm(png_dirs):
    img = cv2.imread(png_dir)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = 255*(gray < 128).astype(np.uint8)
    coords = cv2.findNonZero(gray)
    x, y, w, h = cv2.boundingRect(coords)
    padding = 20
    rect = img[max(0, y-padding):y+h+padding, max(0, x-padding):x+w+padding]
    cv2.imwrite(png_dir, rect)
