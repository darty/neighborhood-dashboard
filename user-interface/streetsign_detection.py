#import sys
#import getopt
#import os
import urllib

from sklearn.externals import joblib
import cv2
import numpy as np
from skimage.feature import hog

from common import *


clf = joblib.load(os.path.join('detecting',os.path.join('clf','streetsigns-hog-svm.pkl')))

def checkDetectionDone(family, streetview_output_folder):
    family_dir = os.path.join(streetview_output_folder, family)
    if not os.path.exists(streetview_output_folder) or not os.path.exists(family_dir):
        return False
    return True


def getFeatures(imgunsized):
    img = cv2.resize(imgunsized, (64,64))
    hog_image = hog(img, orientations=8, pixels_per_cell=(16, 16),cells_per_block=(1, 1))
    return hog_image

def getImagesFromGSV(family, family_road_data, streetview_output_folder):
    if not os.path.exists(streetview_output_folder):
        os.makedirs(streetview_output_folder)
    family_dir = os.path.join(streetview_output_folder, family)
    if not os.path.exists(family_dir):
        os.makedirs(family_dir)
    fov=120
    pitch = 5 #,-11
    point_count = 0
    point_data = []
    for point,headings in family_road_data:
        lat,lon = point
        h_count = 0
        heading_data = []
        for h in headings:
            fname = str(family) + '_' + str(point_count) + '_' + str(h_count) + '.jpg'
            imgname = os.path.join(family_dir, fname)
            if not os.path.isfile(imgname):
                gsv_base_url = "http://maps.googleapis.com/maps/api/streetview?size=640x360&location="+str(lat)+","+str(lon)
                gsv_url = gsv_base_url + "&fov="+str(fov) + "&heading="+str(h) + "&pitch=" + str(pitch) +"&key=" + GSV_KEY
                urllib.urlretrieve(gsv_url, imgname)
                print "Downloaded %s" % imgname
                heading_data.append(fname)
            else:
                print "Image already exist %s" % imgname
            h_count += 1
        point_data.append([point,heading_data])
        point_count += 1
    return point_data

def detectStreetsigns(family, point_data, streetview_output_folder):
    family_dir = os.path.join(streetview_output_folder, family)
    result = {}
    point_count = 0
    for point,heading_data in point_data:
        result[point_count] = {'point' : point, 'images': [], 'detections': [], 'features': []}
        for fname in heading_data:
            result[point_count]['images'].append(os.path.join(family, fname))
            img_filename = os.path.join(family_dir, fname)
            img_data = cv2.imread(img_filename)
            img_resize = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
            scalefactor = 4
            img_resize = cv2.resize(img_resize,(0,0),fx=scalefactor,fy=scalefactor, interpolation=cv2.INTER_CUBIC)
            h,w = np.shape(img_resize)
            ws,hs=64,64
            boxes = []
            while scalefactor >= 1:
                # print "Scalefactor %s" % scalefactor
                for x in range(ws,w-ws,int(8*scalefactor)):
                    for y in range(hs,h-hs,int(8*scalefactor)):
                        if x+ws <= w and y+hs <= h:
                            p = clf.predict_proba(getFeatures(img_resize[y:y+hs,x:x+ws]))[0][1]
                            if p >= 0.9999999999:
                                x1=x*(1./scalefactor)
                                y1=y*(1./scalefactor)
                                scale = ws*(1./scalefactor)
                                boxes.append(np.array([x1,y1,x1+scale,y1+scale,p,scalefactor]))
                                # print scalefactor, x, y, x1, y1, scale
                scalefactor *= 0.5
                img_resize = cv2.resize(img_resize,(0,0),fx=0.5,fy=0.5, interpolation=cv2.INTER_CUBIC)
                h,w = np.shape(img_resize)
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
                #print "******* final rects *****************"
                for r in results:
                    crop_img = img_data[r[1]:r[3], r[0]:r[2]]
                    img_new_filename = fname.split('.')[0]+'_'+str(c)+'_ss.jpg'
                    cv2.imwrite(os.path.join(family_dir, img_new_filename),crop_img)
                    result[point_count]['features'].append(os.path.join(family, img_new_filename))
                    cv2.rectangle(img_data, (r[0],r[1]),(r[2],r[3]),(0,0,255))
                    #print r
                    c+=1
                print 'Detected %s features in %s' % (c, img_filename)
            else:
                print "No Streetsign in %s" % img_filename
            detected_file_name = fname.split('.')[0]+'_detection.png'
            cv2.imwrite(os.path.join(family_dir, detected_file_name),img_data)
            result[point_count]['detections'].append(os.path.join(family, detected_file_name))
        point_count += 1
    return result

def determineStreetSigns(family, family_point_data, streetview_output_folder):
    print 'Determining Street Signs for %s' % (family)
    data = getImagesFromGSV(family, family_point_data, streetview_output_folder)
    result = detectStreetsigns(family, data, streetview_output_folder)
    print result
    return result
