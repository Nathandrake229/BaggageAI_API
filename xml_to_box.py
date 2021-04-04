import xml.etree.ElementTree as ET
from cv2 import cv2

def parseXML(xmlfile, path):
  
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    newsitems = []
    XY = []
    Name = []
    image = cv2.imread(path)
    for item in root.findall('object'):
        for it in item.findall('bndbox'):
            xy = []
            for coord in it:
                xy.append(coord.text)
            XY.append(xy)
    for item in root.findall('object'):
        for it in item.findall('name'):
            Name .append(it.text)
            
    for i in range(len(XY)):
        x = int(XY[i][0])
        y = int(XY[i][1])
        w = int(XY[i][2]) - x
        h = int(XY[i][3]) - y
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)            
        cv2.putText(image, Name[i], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
    #cv2.imshow("Image", image)
    #cv2.waitKey()
    path1 = "C:/work/PYTHON/BaggageAI_API/static/"
    cv2.imwrite(path1 + path.split('/')[-1].split('.')[0] + '_1.jpg', image)
    return [XY, Name, path.split('/')[-1].split('.')[0] + '_1.jpg']

#ewsitems = parseXML('C:\\work\\PYTHON\\P00X000-2019092701425.xml', 'C:\\work\\PYTHON\\P00X000-2019092701425.jpg')