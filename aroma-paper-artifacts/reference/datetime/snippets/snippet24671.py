import random
from os import listdir
from PIL import Image
from datetime import datetime


def writeDataFile(inputImagePath, outputImagePath, inputImageFiles, outputImageFiles, dataFileName):
    dataFile = open(dataFileName, 'w')
    rectSize = 5
    linesCount = 0
    linesLimit = 200000
    linesCountPerImage = 0
    linesLimitPerImage = ((linesLimit / len(inputImageFiles)) + 1)
    for i in range(len(inputImageFiles)):
        print((str(datetime.now()) + ': processing image'), i)
        linesCountPerImage = 0
        inputImage = Image.open(((inputImagePath + '/') + inputImageFiles[i]))
        (inputImageXSize, inputImageYSize) = inputImage.size
        outputImage = Image.open(((outputImagePath + '/') + outputImageFiles[i]))
        (outputImageXSize, outputImageYSize) = outputImage.size
        outputImagePixels = outputImage.load()
        if ((inputImageXSize != outputImageXSize) or (inputImageYSize != outputImageYSize)):
            raise Exception('train inputImage and outputImage mismatch at index', str(i))
        outputImageRoadPixelsArr = []
        outputImageNonRoadPixelsArr = []
        for x in range((rectSize // 2), (inputImageXSize - (rectSize // 2))):
            for y in range((rectSize // 2), (inputImageYSize - (rectSize // 2))):
                isRoadPixel = outputImagePixels[(x, y)]
                if isRoadPixel:
                    outputImageRoadPixelsArr.append((x, y))
                else:
                    outputImageNonRoadPixelsArr.append((x, y))
        random.shuffle(outputImageRoadPixelsArr)
        random.shuffle(outputImageNonRoadPixelsArr)
        for m in range(len(outputImageRoadPixelsArr)):
            if (linesCountPerImage >= linesLimitPerImage):
                break
            if (((m * 2) + 1) >= len(outputImageNonRoadPixelsArr)):
                break
            x = outputImageRoadPixelsArr[m][0]
            y = outputImageRoadPixelsArr[m][1]
            rect = ((x - (rectSize // 2)), (y - (rectSize // 2)), ((x + (rectSize // 2)) + 1), ((y + (rectSize // 2)) + 1))
            subImage = inputImage.crop(rect).load()
            line = ''
            for i in range(rectSize):
                for j in range(rectSize):
                    line += (str(subImage[(i, j)][0]) + ',')
                    line += (str(subImage[(i, j)][1]) + ',')
                    line += (str(subImage[(i, j)][2]) + ',')
            line += (str(1) + '\n')
            linesCount += 1
            linesCountPerImage += 1
            dataFile.write(line)
            for n in range(2):
                x = outputImageNonRoadPixelsArr[((m * 2) + n)][0]
                y = outputImageNonRoadPixelsArr[((m * 2) + n)][1]
                rect = ((x - (rectSize // 2)), (y - (rectSize // 2)), ((x + (rectSize // 2)) + 1), ((y + (rectSize // 2)) + 1))
                subImage = inputImage.crop(rect).load()
                line = ''
                for i in range(rectSize):
                    for j in range(rectSize):
                        line += (str(subImage[(i, j)][0]) + ',')
                        line += (str(subImage[(i, j)][1]) + ',')
                        line += (str(subImage[(i, j)][2]) + ',')
                line += (str(0) + '\n')
                linesCount += 1
                linesCountPerImage += 1
                dataFile.write(line)
    print((((str(datetime.now()) + ': ') + dataFileName) + ' linesCount:'), linesCount)
