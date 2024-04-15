
from PIL import Image
import random
import cv2
import numpy as np
import colour
  
# Opening the primary image (used in background) 
imgBack = Image.open(r"AI Project\DistantMountains.jpg") 

#crop the background image to the area behind the rat
imgBackcrop = imgBack.crop((0, 1000, 164, 1062))
rat = []
fitnessArray = []
fittestRats = []
population = 20
mostFit = population // 2

for x in range(population):
    # Opening the secondary image (overlay image) 
    rat.append(Image.open(r"AI Project/Rat.png"))

fitness = 0
#gets pallet of background image
def getPalette(img):
    reduced = img.convert("P", palette=Image.Palette.WEB) # convert to web palette (216 colors)
    palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
    palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
    color_count.sort(reverse=True) #sort color frequency in descending order
    return color_count

def newColor(color_count):
    new_color = color_count[random.randint(0, len(color_count)-1)][1]
    return new_color

#replaces the color of the rat with the colors of the background randomly at generation 1
def colorRat(new_color, img):
    # Get the size of the image
    width = int(img.width)
    height = int(img.height)


    #Process every pixel
    for x in range(width):
        for y in range(height):
            current_color = img.getpixel( (x,y) )
            if current_color != (0, 0, 0, 0):

                    img.putpixel( (x,y), (new_color[0], new_color[1], new_color[2]))


#finds the difference in color between the rat and the background and uses that as the fitness value  
def calcFitness(img):
     
#     #save the crop and recolored rat
     imgBackcrop.save(r"AI Project\Temp\crop.jpg")
     img.save(r"AI Project\Temp\coloredRat.png")
#     #open them in cv2 (might change this down the line if it takes to long)
     image1_rgb = cv2.imread(r"AI Project\Temp\crop.jpg")
     image2_rgb = cv2.imread(r"AI Project\Temp\coloredRat.png")
#     #convert the RGB values to lab
     image1_lab = cv2.cvtColor(image1_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
     image2_lab = cv2.cvtColor(image2_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
#     #get the difference of the lab values between the 2 images
     delta_E = colour.delta_E(image1_lab, image2_lab)
#     #get the mean of the difference
     mean = float(np.mean(delta_E))
     #calculate fitness value of color difference
     #fitness = 100 * (mean**2 - mean)**2 + (1 - mean)**2
     fitness = mean / 100

     print(fitness)
     return fitness
#finds the most fit rat in the population
def getMostFit():
    fittestRats.clear()
    tempBest = fitnessArray[0]
    tempBestIndex = 0
    for x in range(mostFit):
        for y in range(len(fitnessArray)):
            if(tempBest > fitnessArray[y]):
                tempBest = fitnessArray[y]
                tempBestIndex = y
                print(tempBestIndex)
        fittestRats.append(rat[tempBestIndex])
        rat.pop(tempBestIndex)
        fitnessArray.pop(tempBestIndex)
        tempBest = fitnessArray[0]
        tempBestIndex = 0
        

def mutate():
    #mutate the color of the rat
    return

def crossover():
    #crossover the color of the rat
    for x in range(len(fittestRats)-5):   
        rat1 = getPalette(fittestRats[x])
        rat2 = getPalette(fittestRats[x + 5])
        
        for i in range(2):
            
            color = []   
            ran = random.randint(1,99)
            if ran <= 33:
                color.append(rat1[1][1][0])
                color.append(rat2[1][1][1])
                color.append(rat2[1][1][2])
                
            elif ran > 33 and ran <= 66:
                color.append(rat1[1][1][1])
                color.append(rat2[1][1][0])
                color.append(rat2[1][1][2])
            else:
                color.append(rat1[1][1][2])
                color.append(rat2[1][1][0])
                color.append(rat2[1][1][1])
              
            rat.append(Image.open(r"AI Project/Rat.png"))      
            colorRat(color, rat[x + 10 + i])
    
    
    return

def select():
    #select the best color for the rat
    if(fitness < 0.1):
        pasteImg()
        showImg()
    return

def pasteImg(img):
    # Pasting img image on top of imgBack  
    # starting at coordinates (0, 0) 
    imgBack.paste(img, (0,1000), mask = img) 
    
#shows the best rat and saves it
def showImg():
    imgBack.save(r"AI Project\bestRat.jpg")
    imgBack.show()
    quit()

colors = getPalette(imgBack)

for x in range(2):
    print(len(rat))
    for i in range(population):  
        colorRat(newColor(colors), rat[i])
        fitnessArray.append(calcFitness(rat[i]))
    getMostFit() 
    
    fitnessArray.clear()
    crossover()   
        
    #for x in range(mostFit):
     #   crossover(fitness[x], fitness[x+1])
