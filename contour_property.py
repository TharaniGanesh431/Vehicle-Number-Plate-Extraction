import cv2
import math

import contour_specification

def distanceBetweenContour(contour1, contour2):
    X = abs(contour1.CenterX - contour2.CenterX)
    Y = abs(contour1.CenterY - contour2.CenterY)

    return math.sqrt((X ** 2) + (Y ** 2))

def angleBetweenContour(contour1, contour2):
    Adj = float(abs(contour1.CenterX - contour2.CenterX))
    Opp = float(abs(contour1.CenterY - contour2.CenterY))

    if Adj != 0.0:                          
        AngleInRad = math.atan(Opp / Adj)      
    else:
        AngleInRad = 1.5708                        

    AngleInDeg = AngleInRad * (180.0 / math.pi)      

    return AngleInDeg


def borderAroundContour(img, contour):
    border = contour_specification.Plates()          

    contour.sort(key = lambda matchingCon: matchingCon.CenterX)      

          
    centerX = (contour[0].CenterX + contour[len(contour) - 1].CenterX) / 2.0
    centerY = (contour[0].CenterY + contour[len(contour) - 1].CenterY) / 2.0

    center = centerX, centerY

          
    width = int((contour[len(contour) - 1].X + contour[len(contour) - 1].Width - contour[0].X) * 1.3)

    totalHeight = 0

    for i in contour:
        totalHeight = totalHeight + i.Height

    avgHeight = totalHeight / len(contour)

    height = int(avgHeight * 1.5)

          
    opposite = contour[len(contour) - 1].CenterY - contour[0].CenterY

    hypotenuse = distanceBetweenContour(contour[0], contour[len(contour) - 1])
    correctionAngleInRad = math.asin(opposite / hypotenuse)
    correctionAngleInDeg = correctionAngleInRad * (180.0 / math.pi)

          
    border.Location = ( tuple(center), (width, height), correctionAngleInDeg )

    rotationMatrix = cv2.getRotationMatrix2D(tuple(center), correctionAngleInDeg, 1.0)

    img_height, img_width,_ = img.shape    

    imgRotated = cv2.warpAffine(img, rotationMatrix, (img_width, img_height))     

    imgCropped = cv2.getRectSubPix(imgRotated, (width, height), tuple(center))

    border.Plate = imgCropped        

    return border

def removeOverlappingContour(contour):
    removedContour = list(contour)               

    for currentContour in contour:
        for otherContour in contour:
            if currentContour != otherContour:       
                                                                        
                if distanceBetweenContour(currentContour, otherContour) < (currentContour.diagonalSize * 0.3):
                                
                    if currentContour.Area < otherContour.Area:        
                        if currentContour in removedContour:           
                            removedContour.remove(currentContour)      
                    else:                                              
                        if otherContour in removedContour:             
                            removedContour.remove(otherContour)        

    return removedContour

