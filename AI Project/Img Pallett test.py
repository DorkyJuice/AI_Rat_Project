
from PIL import Image
import random
import cv2
import numpy as np
import colour
  
# Opening the primary image (used in background) 
imgBack = Image.open(r"C:\Users\casey\OneDrive\Documents\GitHub\AI_Rat_Project\AI Project\DistantMountains.jpg") 

#crop the background image to the area behind the rat
imgBackcrop = imgBack.crop((0, 1000, 164, 1062))
rat = []
fitnessArray = []
fittestRats = []
population = 20
mostFit = population // 2

for x in range(population):
    # Opening the secondary image (overlay image) 
    rat.append(Image.open(r"C:\Users\casey\OneDrive\Documents\GitHub\AI_Rat_Project\AI Project\Rat.png"))

fitness = 0

def getPalette(img):
    reduced = img.convert("P", palette=Image.Palette.WEB) # convert to web palette (216 colors)
    palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
    palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
    color_count.sort(reverse=True) #sort color frequency in descending order
    return color_count

def colorRat(color_count, img):
    # Get the size of the image
    width = int(img.width)
    height = int(img.height)
    new_color = color_count[random.randint(0, len(color_count)-1)][1]

    #Process every pixel
    for x in range(width):
        for y in range(height):
            current_color = img.getpixel( (x,y) )
            if current_color != (0, 0, 0, 0):
                    
                    img.putpixel( (x,y), (new_color[0], new_color[1], new_color[2]))

def calcFitness(img):
#     #save the crop and recolored rat
     imgBackcrop.save(r"C:\Users\casey\OneDrive\Documents\GitHub\AI_Rat_Project\AI Project\Temp\crop.jpg")
     img.save(r"C:\Users\casey\OneDrive\Documents\GitHub\AI_Rat_Project\AI Project\Temp\coloredRat.png")
#     #open them in cv2 (might change this down the line if it takes to long)
     image1_rgb = cv2.imread(r"C:\Users\casey\OneDrive\Documents\GitHub\AI_Rat_Project\AI Project\Temp\crop.jpg")
     image2_rgb = cv2.imread(r"C:\Users\casey\OneDrive\Documents\GitHub\AI_Rat_Project\AI Project\Temp\coloredRat.png")
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

def getMostFit():
    #find most fit out of population
    tempBest = fitnessArray[0]
    tempBestIndex = 0
    for x in range(mostFit):
        for y in range(fitnessArray.len()):
            if(tempBest < fitnessArray[y]):
                tempBest = fitnessArray[y]
                tempBestIndex = y
        fittestRats.append(rat[tempBestIndex])
        rat.pop[tempBestIndex]
        fitnessArray.pop[tempBestIndex]
        

def mutate():
    #mutate the color of the rat
    return

def crossover():
    #crossover the color of the rat
    
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

def showImg():
    imgBack.save(r"C:\Users\casey\OneDrive\Documents\GitHub\AI_Rat_Project\AI Project\imgBack.jpg")
    imgBack.show()
    quit()

colors = getPalette(imgBack)

while True:
    for x in range(population):
        colorRat(colors, rat[x])
       ## fitness.sort
        fitness.append(calcFitness(rat[x]))
    getMostFit()    
    print(fittestRats)
    break
        
    #for x in range(mostFit):
     #   crossover(fitness[x], fitness[x+1])
