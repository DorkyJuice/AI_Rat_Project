
from PIL import Image
import random
import cv2
import numpy as np
import colour
  
# Opening the primary image (used in background) 
img1 = Image.open(r"C:\AI Project\DistantMountains.jpg") 

#crop the background image to the area behind the rat
img1crop = img1.crop((0, 1000, 164, 1062))
  
# Opening the secondary image (overlay image) 
img2 = Image.open(r"C:\AI Project\Rat.png") 

def getPalette():
    reduced = img1.convert("P", palette=Image.Palette.WEB) # convert to web palette (216 colors)
    palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
    palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
    color_count.sort(reverse=True) #sort color frequency in descending order
    return color_count

def colorRat(color_count):
    # Get the size of the image
    width = int(img2.width)
    height = int(img2.height)

    #Process every pixel
    for x in range(width):
        for y in range(height):
            current_color = img2.getpixel( (x,y) )
            if current_color != (0, 0, 0, 0):
                    new_color = color_count[random.randint(0, len(color_count)-1)][1]
                    img2.putpixel( (x,y), (new_color[0], new_color[1], new_color[2]))

def calcFitness():
    #save the crop and recolored rat
    img1crop.save("C:\AI Project\Temp\crop.jpg")
    img2.save("C:\AI Project\Temp\coloredRat.png")
    #open them in cv2 (might change this down the line if it takes to long)
    image1_rgb = cv2.imread("C:\AI Project\Temp\crop.jpg")
    image2_rgb = cv2.imread("C:\AI Project\Temp\coloredRat.png")
    #convert the RGB values to lab
    image1_lab = cv2.cvtColor(image1_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
    image2_lab = cv2.cvtColor(image2_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
    #get the difference of the lab values between the 2 images
    delta_E = colour.delta_E(image1_lab, image2_lab)
    #get the mean of the difference
    mean = float(np.mean(delta_E))
    #calculate fitness value of color difference
    fitness = 100 * (mean**2 - mean)**2 + (1 - mean)**2

    print(fitness)
    return fitness

def pasteImg():
    # Pasting img2 image on top of img1  
    # starting at coordinates (0, 0) 
    img1.paste(img2, (0,1000), mask = img2) 

def showImg():
    img1.show()

colorRat(getPalette())
calcFitness()
pasteImg()
showImg()