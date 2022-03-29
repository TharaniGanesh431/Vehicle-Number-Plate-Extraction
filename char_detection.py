import cv2
import math

import contour_property

def checkChar(contour):
    if (contour.Area > 80 and
    contour.Width > 2 and
    contour.Height > 8 and
    0.25 < contour.aspectRatio and
        contour.aspectRatio < 1):
        
        return True
    else:
        return False

def matchChar(contour):
    char_list = []
    for c in contour:           
        char = findMatchChar(c,contour)

        char.append(c)

        if len(char) < 3:
            continue
        
        char_list.append(char)     

        unmatch_char = []

        unmatch_char = list(set(contour) - set(char))

        for i in matchChar(unmatch_char):
            char_list.append(i)    
        break
    
    return char_list

def findMatchChar(char, listOfChars):
    matching_char = []               

    for i in listOfChars:              
        if i == char:    
            continue                            
       
        distanceBetweenChars = contour_property.distanceBetweenContour(char, i)

        angleBetweenChars = contour_property.angleBetweenContour(char, i)

        changeInArea = float(abs(i.Area - char.Area)) / float(char.Area)

        changeInWidth = float(abs(i.Width - char.Width)) / float(char.Width)
        changeInHeight = float(abs(i.Height - char.Height)) / float(char.Height)

        if (distanceBetweenChars < (char.diagonalSize * 5.0) and
            angleBetweenChars < 12.0 and
            changeInArea < 5.0 and
            changeInWidth < 0.8 and
            changeInHeight < 0.2):

            matching_char.append(i)
    return matching_char                  
