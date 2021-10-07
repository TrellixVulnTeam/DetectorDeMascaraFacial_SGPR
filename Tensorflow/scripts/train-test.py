import os
import sys
from shutil import copyfile
import xml.etree.ElementTree as ET
from random import randint

imagePath = ''
totrainYes = 0.9
totrainNo = 0.9

if len(sys.argv) > 1:
    if len(sys.argv) == 2:
        imagePath = sys.argv[1]+'/'
    elif len(sys.argv) == 3:
        imagePath = sys.argv[1]+'/'
        totrainYes = float(sys.argv[2])
        totrainNo = float(sys.argv[2])
    elif len(sys.argv) == 4:
        imagePath = sys.argv[1]+'/'
        totrainYes = float(sys.argv[2])
        totrainNo = float(sys.argv[3])
    else:
        print('Usage: {} IMAGE_PATH [percentageToTrainYes] [percentageToTrainNo]\nor {} IMAGE_PATH [percentageToTrain]\nor {} IMAGE_PATH\nor {}'.format(sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0]))

allimagesPath = imagePath+'allimages/'
testPath = imagePath+'test/'
trainPath = imagePath+'train/'

tagMascara = 'Com Mascara'
tagSemMascara = 'Sem Mascara'

allimages = os.listdir(allimagesPath)

maskNum = 0
noMaskNum = 0

mask = []
noMask = []

for file in allimages:
    if file.endswith(".xml"):
        try:
            tree = ET.parse(allimagesPath+file)
            imgName = tree.getroot()[1].text
            tag = tree.getroot()[6][0].text
            if tag == tagMascara:
                maskNum += 1
                mask.append(imgName)
            elif tag == tagSemMascara:
                noMaskNum += 1
                noMask.append(imgName)
            else:
                print(tag)
        except:
            print('')
            #print('Erro - {}-{}'.format(file, tag))

print('Mask: {}'.format(maskNum))
print('NoMask: {}'.format(noMaskNum))

while len(mask) > totrainYes*maskNum:
    # print(len(mask))
    index = randint(0, len(mask)-1)
    img = mask[index]
    xml = img.split('.')[0]+'.xml'
    mask.remove(img)
    copyfile(allimagesPath+img, testPath+img)
    copyfile(allimagesPath+xml, testPath+xml)

while len(noMask) > totrainNo*noMaskNum:
    # print(len(noMask))
    index = randint(0, len(noMask)-1)
    img = noMask[index]
    xml = img.split('.')[0]+'.xml'
    noMask.remove(img)
    copyfile(allimagesPath+img, testPath+img)
    copyfile(allimagesPath+xml, testPath+xml)

while len(mask) > 0:
    index = randint(0, len(mask)-1)
    img = mask[index]
    xml = img.split('.')[0]+'.xml'
    mask.remove(img)
    copyfile(allimagesPath+img, trainPath+img)
    copyfile(allimagesPath+xml, trainPath+xml)

while len(noMask) > 0:
    index = randint(0, len(noMask)-1)
    img = noMask[index]
    xml = img.split('.')[0]+'.xml'
    noMask.remove(img)
    copyfile(allimagesPath+img, trainPath+img)
    copyfile(allimagesPath+xml, trainPath+xml)

print('Done')