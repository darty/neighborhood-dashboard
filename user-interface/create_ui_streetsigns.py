# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 09:07:39 2015

@author: nr
"""

__author__ = 'ddegraen nr'

import sys
import getopt
import os
import urllib

from pykml import parser
from sklearn.externals import joblib
import cv2 
import numpy as np
from skimage.feature import hog

clf = joblib.load(os.path.join('detecting',os.path.join('clf','streetsigns-hog-svm.pkl')))

def printUsage():
    print '###########################################################################################################'
    print os.path.basename(__file__), '-k <kmlfile> -s -d'
    print '###########################################################################################################'
    print '   -k <kmlfile>: open kml'
    print '   -s : save to html'
    print '   -d : detect streetsigns'

from common_private import GSV_KEY

def getImagesFromGSV(kmlfile):
    svdirectory = "streetviewimages"
    if not os.path.exists(svdirectory):
        os.makedirs(svdirectory)
    family = os.path.basename(kmlfile).split('.')[0]
    fov=120
    pitches = [5]#,-11
    with open(kmlfile) as f:
        doc = parser.parse(f)
        root = doc.getroot()
        for placemark in root.Document.Placemark:
            pt = placemark.find(".//{http://earth.google.com/kml/2.1}Point")
            name = placemark.name
            if pt is not None:   
                lon,lat,x = placemark.Point.coordinates.text.strip().split(',')
                for data in placemark.ExtendedData.findall(".//*[@name='headings']/{http://earth.google.com/kml/2.1}value"):
                    headings = data.text.strip().split(",")
                    h_count = 0
                    for h in headings:
                        for pitch in pitches:
                            imgname = str(family) + '_' + str(name) + '_' + str(h_count) + '.jpg'    
                            p = os.path.join(svdirectory,imgname)
                            if not os.path.isfile(p):
                                gsv_base_url = "http://maps.googleapis.com/maps/api/streetview?size=640x360&location="+str(lat)+","+str(lon)
                                gsv_url = gsv_base_url + "&fov="+str(fov) + "&heading="+str(h) + "&pitch=" + str(pitch) +"&key=" + GSV_KEY
                                urllib.urlretrieve(gsv_url, p)
                                print "Downloaded", p
                            else:
                                print p, "Image already exist"
                        h_count+=1
    
    
def getFeatures(imgunsized):
    img = cv2.resize(imgunsized, (64,64))
    hog_image = hog(img, orientations=8, pixels_per_cell=(16, 16),cells_per_block=(1, 1))
    return hog_image

def getImagesfromKML(kmlfile):
    imgs = []
    family = os.path.basename(kmlfile).split('.')[0]
    svdirectory = "streetviewimages"
    pitches = [2]#,-11
    with open(kmlfile) as f:
        doc = parser.parse(f)
        root = doc.getroot()
        for placemark in root.Document.Placemark:
            name = placemark.name
            pt = placemark.find(".//{http://earth.google.com/kml/2.1}Point")
            if pt is not None:   
                lon,lat,x = placemark.Point.coordinates.text.strip().split(',')
                for data in placemark.ExtendedData.findall(".//*[@name='headings']/{http://earth.google.com/kml/2.1}value"):
                    headings = data.text.strip().split(",")
                    head = 0
                    for h in headings:
                        for pitch in pitches:
                            i = str(family) + '_' + str(name) + '_' + str(head) + '.jpg'           
                            imgname = os.path.join(svdirectory,i)
                            imgs.append(imgname)
                        head+=1
    return imgs


def detectStreetsigns(kmlfile):
    imgs = getImagesfromKML(kmlfile)
    for imgname in imgs:
        imgorig = cv2.imread(imgname)
        img = cv2.cvtColor(imgorig, cv2.COLOR_BGR2GRAY)
        scalefactor = 4
        img = cv2.resize(img,(0,0),fx=scalefactor,fy=scalefactor, interpolation=cv2.INTER_CUBIC)
        h,w = np.shape(img)
        ws,hs=64,64
        boxes = []
        #while w > ws and h > hs:
        while scalefactor >= 1:
            print "scalefactor",scalefactor
            for x in range(ws,w-ws,int(8*scalefactor)):
                for y in range(hs,h-hs,int(8*scalefactor)):
                    if x+ws <= w and y+hs <= h:
                        p = clf.predict_proba(getFeatures(img[y:y+hs,x:x+ws]))[0][1]
                        if p >= 0.9999999999:
                            x1=x*(1./scalefactor)
                            y1=y*(1./scalefactor)
                            scale = ws*(1./scalefactor)
                            boxes.append(np.array([x1,y1,x1+scale,y1+scale,p,scalefactor]))
                            print scalefactor, x, y, x1, y1, scale
                            
            scalefactor *= 0.5
            img = cv2.resize(img,(0,0),fx=0.5,fy=0.5, interpolation=cv2.INTER_CUBIC)
            h,w = np.shape(img)
        if len(boxes)>0:
            # grab the coordinates of the bounding boxes
            boxes = np.array(boxes)
            x1 = boxes[:,0]
            y1 = boxes[:,1]
            x2 = boxes[:,2]
            y2 = boxes[:,3]
            p = boxes[:,4]
            pick = []
            
            # compute the area of the bounding boxes and sort the bounding
            # boxes by the bottom-right y-coordinate of the bounding box
            area = (x2 - x1 + 1) * (y2 - y1 + 1)
            idxs = np.argsort(p)
            overlapThresh = 0.1
            # keep looping while some indexes still remain in the indexes
            # list
            while len(idxs) > 0:
                # grab the last index in the indexes list and add the
                # index value to the list of picked indexes
                last = len(idxs) - 1
                i = idxs[last]
                pick.append(i)
                xx1 = np.maximum(x1[i], x1[idxs[:last]])
                yy1 = np.maximum(y1[i], y1[idxs[:last]])
                xx2 = np.minimum(x2[i], x2[idxs[:last]])
                yy2 = np.minimum(y2[i], y2[idxs[:last]])
                w = np.maximum(0, xx2 - xx1 + 1)
                h = np.maximum(0, yy2 - yy1 + 1)
                overlap = (w * h) / area[idxs[:last]]
                idxs = np.delete(idxs, np.concatenate(([last], np.where(overlap > overlapThresh)[0])))
            results = boxes[pick].astype("int")
            c = 0
            print "******* final rects *****************"
            for r in results:                
                crop_img = imgorig[r[1]:r[3], r[0]:r[2]]
                cv2.imwrite(imgname.split('.')[0]+'_'+str(c)+'_ss.jpg',crop_img)
                cv2.rectangle(imgorig, (r[0],r[1]),(r[2],r[3]),(0,0,255))
                print r
                c+=1
        else:
            print "No Streetsign in",imgname
        cv2.imwrite(imgname+"_detection.png",imgorig)

def createHTML(kmlfile):
    imgs = getImagesfromKML(kmlfile)
    af = os.listdir("streetviewimages")
    family = os.path.basename(kmlfile).split('.')[0]
    d = [i for i in af if i.startswith(family) and i.endswith("_ss.jpg")]
    html = '<html><style>img {padding: 5px;}</style><body><div class="svimgs">'
    html += str(len(d)) + ' streetsign detected</br>'
    forth = []
    back = []
    for i in imgs:
        head = int(i.split('.')[0].split('_')[2])
        if head==0:
            forth.append(i)
        else:
            back.append(i)
    html += "</br>Forth:</br>"
    for imgname in forth:
        html += '<img src="'+imgname+'" alt="GSV Image"'+imgname+' width="128" height="72" border="0"'+'/>' 
    html += "</br>Back:</br>"
    for imgname in back:
        html += '<img src="'+imgname+'" alt="GSV Image"'+imgname+' width="128" height="72" border="0"'+'/>'             
    html += "</br>Streetsigns:</br>"
    for imgname in d:
        html += '<img src="'+'streetviewimages/'+imgname+'" alt="GSV Image"'+'streetviewimages/'+imgname+' width="64" height="64" border="0"'+'/>'                     
    html += '</div></html></body>'
    f = open(str(family)+'.html', 'w')
    f.write(html)

if __name__ == "__main__":
    kmlfile = ''
    detect = False
    save = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hk:ds",["kmlfile=","detect","save","help"])
        for opt, arg in opts:
            if opt == '-h':
                printUsage()
                sys.exit(0)
            elif opt == '-k':
                kmlfile = arg
            elif opt == '-d':
                detect = True
            elif opt == '-s':
                save = True
        if kmlfile == '':
            printUsage()
        else:
            print "Downloading Images"
            getImagesFromGSV(kmlfile)
            if detect:
                print "Detecting Streetsigns"
                detectStreetsigns(kmlfile)
            if save:
                print "Saving HTML"
                createHTML(kmlfile)
                
    except getopt.GetoptError:
        print 'Error: '
        printUsage()
        sys.exit(2)
