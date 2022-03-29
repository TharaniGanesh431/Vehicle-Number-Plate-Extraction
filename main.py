import cv2
import numpy as np
import math
import sys
import tkinter as tk
from tkinter import *

import image_property
import char_recognition 
import char_detection
import contour_property

import contour_specification


def num_plate(org):
    
    plates = []

    gray=image_property.grayScale(org)

    blur = cv2.GaussianBlur(image_property.maximizeContrast(gray), (5, 5), 0)
    threshold = cv2.adaptiveThreshold(blur, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)

    contours,_= cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    chars=[]
    for i in range(0, len(contours)):                   
        contour=contour_specification.contourProperty(contours[i])
        if char_detection.checkChar(contour):            
            chars.append(contour)
        
    chars = char_detection.matchChar(chars)

    for i in chars:
        plate = contour_property.borderAroundContour(org, i)

        if plate.Plate is not None:
            plates.append(plate)
   
    return plates

def detectCharsInPlates(plate):

    if len(plate) == 0:          
        return plate    

    for p in plate:

        p.gray=image_property.grayScale(p.Plate)

        blur = cv2.GaussianBlur(image_property.maximizeContrast(p.gray), (5, 5), 0)
        p.threshold = cv2.adaptiveThreshold(blur, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 9)    
                
        chars = []
        contours, _ = cv2.findContours(p.threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:                        
            contour = contour_specification.contourProperty(c)
            if char_detection.checkChar(contour):
                chars.append(contour)
        
        chars = char_detection.matchChar(chars)
        
        if (len(chars) == 0):       
            continue
        
        for i in range(0, len(chars)):                           
            chars[i].sort(key = lambda matchingChar: matchingChar.CenterX)      
            chars[i] = contour_property.removeOverlappingContour(chars[i])          

        long_char = 0

               
        for i in range(0, len(chars)):
            if len(chars[i]) > long_char:
                long_char = len(chars[i])
                index = i
    
        p.Chars = char_recognition.recognizeChar(p.threshold, chars[index])
           
    return plate






def mainpart():
    if char_recognition.loadAndTrainML() == False:              
        print("\nerror: Machine traning Failed\n")
        sys.exit()

    image=imgfile.get()
    org  = cv2.imread(image)

    if org is None:                            
        print("\n image not read from file \n\n")
        sys.exit()

    plates = num_plate(org)

    global  char_plate
    char_plate = detectCharsInPlates(plates)

    if len(char_plate) == 0:                          
        print("\nNo Number plates were detected\n")
    
    else:                                   
    
        char_plate.sort(key = lambda Plates: len(Plates.Chars), reverse = True)

        if len(char_plate[0].Chars) == 0:               
            print("\nNo characters were detected\n\n")

        outputscreen()

        #print("\nNumber plate read from image = " + char_plate[0].Chars + "\n")
        #print(char_plate[0].Chars)

        cv2.waitKey(0)


def outputscreen():
    label3=Label(root,text="THE NUMBER READ FROM THE IMAGE IS ",font=('Cambria','15','bold')).place(x=200,y=590)
    label2=Label(root,text=char_plate[0].Chars,font=('Cambria','25','bold'),fg="Red").place(x=700,y=585)
    btn2bg = Frame(root, background = 'BLACK', borderwidth = 3, relief = FLAT)
    btn2=Button(btn2bg,text="CLOSE",command=root.destroy,font=('Cambria','15','bold'))
    btn2bg.place(x=700,y=700)
    btn2.pack()


def mainscreen():
    global root  
    root=Tk()
    root.title("Image acquisition")
    root.geometry("1500x900")
    global imgfile
    imgfile=StringVar()
    label1=Label(root,text="NUMBER PLATE DETECTION & RECOGNITION",fg="White",bg="Black",height=3,width=720,font=('Cambria','28','bold'))
    label1.pack()
    label2=Label(root,text="ENTER THE NAME/LOCATION OF THE IMAGE",font=('Cambria','15','bold')).place(x=200,y=390)
    entrybg = Frame(root, background = 'BLACK', borderwidth = 3, relief = FLAT)
    entry1=Entry(entrybg,width=40,font=('10'),textvar=imgfile)
    entrybg.place(x=700,y=390)
    entry1.pack(ipady=4)
    btn1bg = Frame(root, background = 'BLACK', borderwidth = 3, relief = FLAT)
    btn1=Button(btn1bg,text="SUBMIT",command=mainpart,font=('Cambria','15','bold'))
    btn1bg.place(x=600,y=700)
    btn1.pack()
    

mainscreen()


























