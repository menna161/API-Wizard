import random
from os import listdir
from PIL import Image
from datetime import datetime


def writeDataFileOld(inputImagePath, outputImagePath, inputImageFiles, outputImageFiles, dataFileName):
    dataFile = open(dataFileName, 'w')
    roadPixel = 1
    nonroadPixel = 0
    neededPixel = 0
    rectSize = 5
    for i in range(len(inputImageFiles)):
        print((str(datetime.now()) + ': processing image'), i)
        inputImage = Image.open(((inputImagePath + '/') + inputImageFiles[i]))
        (inputImageXSize, inputImageYSize) = inputImage.size
        inputImagePixels = inputImage.load()
        outputImage = Image.open(((outputImagePath + '/') + outputImageFiles[i]))
        (outputImageXSize, outputImageYSize) = outputImage.size
        outputImagePixels = outputImage.load()
        if ((inputImageXSize != outputImageXSize) or (inputImageYSize != outputImageYSize)):
            raise Exception('train inputImage and outputImage mismatch at index', str(i))
        for x in range((rectSize // 2), (inputImageXSize - (rectSize // 2))):
            for y in range((rectSize // 2), (inputImageYSize - (rectSize // 2))):
                isRoadPixel = outputImagePixels[(x, y)]
                if (isRoadPixel and (neededPixel != roadPixel)):
                    continue
                if ((not isRoadPixel) and (neededPixel == roadPixel)):
                    continue
                neededPixel = ((neededPixel + 1) % 3)
                rect = ((x - (rectSize // 2)), (y - (rectSize // 2)), ((x + (rectSize // 2)) + 1), ((y + (rectSize // 2)) + 1))
                subImage = inputImage.crop(rect).load()
                line = ''
                for i in range(rectSize):
                    for j in range(rectSize):
                        line += (str(subImage[(i, j)][0]) + ',')
                        line += (str(subImage[(i, j)][1]) + ',')
                        line += (str(subImage[(i, j)][2]) + ',')
                line += (str((roadPixel if isRoadPixel else nonroadPixel)) + '\n')
                dataFile.write(line)
