###############################################

#Assignment 1: Transformation
#BRINGING THE PAST TO LIFE
#Code written by Laura Whelan

###############################################
#============================================

#INTRODUCTION:
# Using image processing skills to restore light damaged photos to their former glory


#ASSIGNMENT:
#1. Convert to an appropriate colourspace to exaggerate the difference between damaged and undamaged areas so as to identify the damage.
#2. Enhance the images to increase contrast and definition.
#3. Remove any colour introduced by damage.
#4. The final image should be an enhanced version of the original, with little or no distinction between damaged and undamaged parts.


#STRUCTURE OF CODE:
#1. Import the necessary packages

#2. Read in the image

#3. Convert Image to appropriate colourspace for edge detection

#4a. If lines detected: 
    # The code dyanmically locates any faded rectangular areas in the image using the canny function,
    # and using the HoughLineP function, the corners of this rectangular area can be identified.
    # using those corners, the difference can be found in the greyscale image.
    # This difference can then be subtracted from the greysclae image, to give the output image
    # The output image is showed, alongside the original image
    
#4b. If no lines detected: remove saturation, blur, shaprne and then weighted addd the blur and sharpened images to get new output, show the relevant output images
    #The code converts the image to HSV and removes the saturation to remove any staining,
    # The image is blurred, then sharpened, and the blurred image is added to the sharpened image using the addWeighted function
    # The added image result is the output, and shown alongside the original image.
    
#5. Final Results and Comments


#REFERENCES
#[1] Docs.opencv.org. 2020. Opencv: Hough Line Transform. [online] 
#    Available at: <https://docs.opencv.org/3.4/d6/d10/tutorial_py_houghlines.html> 
#    [Accessed 23 October 2020].

###############################################
#1.============================================

import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui

#2.============================================
print('select an image file')
f = easygui.fileopenbox()
I = cv2.imread(f)

# I = cv2.imread("Faded.jpg")
# I = cv2.imread("Damaged.jpg")
Ioriginal=I.copy()
Iline=I.copy()

#3.=============================================

G = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(G,50,150,apertureSize = 3) #[1]
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength=250,maxLineGap=5) #[1]
#print(lines)

#4a.=============================================

if lines is not None:
    lines_array=lines.ravel()
    #print(lines_array)
        
    for line in lines:
        x1,y1,x2,y2 = line[0]
        cv2.line(Iline,(x1,y1),(x2,y2),(0,255,0),2)

    ptl=[lines_array[0],lines_array[5]] #defines point at bottom left (bl)
    ptr=[lines_array[2],lines_array[5]] #defines point at bottom right (br)
    pbl=[lines_array[0],lines_array[1]] #defines point at top left (tl)
    pbr=[lines_array[2],lines_array[1]] #defines point at top right (tr)

    # print('pbl: ' ,pbl)
    # print('pbr: ' ,pbr)
    # print('ptl: ' ,ptl)
    # print('ptr: ' ,ptr)

    pblx=pbl[0] 
    pbly=pbl[1] 
    # print('pblx: ' ,pblx) #bottom left x =57
    # print('pbly: ' ,pbly) #bottom left y =330

    pbrx=pbr[0] 
    pbry=pbr[1] 
    # print('pbrx: ' ,pbrx) #bottom right x =461
    # print('pbry: ' ,pbry) #bottom right y = 330

    ptlx=ptl[0] 
    ptly=ptl[1] 
    # print('ptlx: ' ,ptlx) #top left x =57
    # print('ptly: ' ,ptly)#top left y =4

    ptrx=ptr[0] 
    ptry=ptr[1] 
    # print('ptrx: ' ,ptrx) #top right x =461
    # print('ptry: ' ,ptry) #top right y =4


    diff=G[ptly+20,ptlx+5]-G[ptly+20,ptlx-5] #find the difference between damaged and undamged
    #print('diff: ' ,diff) #diff=31
    output=G.copy()
    output[ptly:pbry,ptlx:pbrx]=G[ptly:pbry,ptlx:pbrx]-diff
    
    output =cv2.cvtColor(output,cv2.COLOR_GRAY2RGB)
   
    cv2.imshow('original',Ioriginal)
    cv2.imshow('canny houghlines',Iline)
    cv2.imshow('output',output)
    key =cv2.waitKey(0)
    
#4b.=============================================

if lines is None:
    HSV = cv2.cvtColor(I, cv2.COLOR_BGR2HSV) 
    HSV[:,:,1]=0 
    colour_removed =cv2.cvtColor(HSV,cv2.COLOR_HSV2RGB)
    
    kernel1 = np.array([[0.0625,0.125,0.0625], [0.125,0.25,0.125], [0.0625,0.125,0.0625]])
    blur1 = cv2.filter2D(colour_removed, -1, kernel1)

    kernel2 = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
    sharp1 = cv2.filter2D(blur1, -1, kernel2)
    
    blur_weight=.7
    sharp_weight = (1.0 - blur_weight)
    gamma = 0 
    output = cv2.addWeighted(blur1, blur_weight, sharp1, sharp_weight, gamma)
    
    
    cv2.imshow('blur', blur1)
    cv2.imshow('sharp', sharp1)
    cv2.imshow('output', output)
    cv2.imshow('original',Ioriginal)
    key =cv2.waitKey(0)

#5.=============================================

cv2.imwrite('Final Output.jpg', output)

#RESULTS FOR FADED IMAGE:
    #The image has significantly improved and has very little trace of the "box" left, 
    #and hasnt lost any significant amount of detailing

#RESULTS FOR DAMAGED IMAGE:
    #The image has imporved with the removal of the yellow staining,
    # however the detail was difficult to keep intact while trying to remove any "blotchiness" 
    # there are some "blotchy" areas that remain visible, but the detail hasnt been significantly lost
