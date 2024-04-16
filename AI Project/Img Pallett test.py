
from PIL import Image
import random
import cv2
import numpy as np
import colour
import pandas as pd
 
# Opening the primary image (used in background) 
imgBack = Image.open(r"AI Project\DistantMountains.jpg") 

#crop the background image to the area behind the rat
imgBackcrop = imgBack.crop((0, 1000, 164, 1062))
rat = []
childRats = []
fitnessArray = []
fittestRats = []
fittestRatsFitness = []
population = 100
mostFit = population // 2

for x in range(population):
    # Opening the secondary image (overlay image) 
    rat.append(Image.open(r"AI Project/Rat.png"))

highestFitness = 1
fittestRat = Image.open(r"AI Project/Rat.png")
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
def colorRat(new_color, img, x, y):
    
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

     #print(fitness)
     
     return fitness
 
#finds the most fit rat in the population
def getMostFit():
    fittestRats.clear()
    fittestRatsFitness.clear()
    tempRats = []
    tempFitness = []
    for i in range(len(rat)):
        tempRats.append(rat[i])
    for i in range(len(fitnessArray)):
        tempFitness.append(fitnessArray[i])
    tempBest = tempFitness[0]
    tempBestIndex = 0
    for x in range(mostFit):
        for y in range(len(tempFitness)):
            if(tempBest > tempFitness[y]):
                tempBest = tempFitness[y]
                tempBestIndex = y
            
        fittestRats.append(rat[tempBestIndex])
        fittestRatsFitness.append(tempFitness[tempBestIndex])
        tempRats.pop(tempBestIndex)
        tempFitness.pop(tempBestIndex)
        tempBest = tempFitness[0]
        tempBestIndex = 0
        

def mutate():
    #mutate the color of the rat
    return random.randint(0,255)

def crossover():
    #crossover the color of the rat
    for j in range(2):
        for i in range(len(fittestRats) - len(fittestRats) // 2):   
            rat1 = getPalette(fittestRats[i])
            rat2 = getPalette(fittestRats[i + len(fittestRats) // 2])
        
            childRats.append(Image.open(r"AI Project/Rat.png"))
            
            # Get the size of the image
            width = int(childRats[i].width)
            height = int(childRats[i].height)
            #Process every pixel
            for x in range(width):
                for y in range(height):
                    current_color = rat[i].getpixel( (x,y) )
                    if current_color != (0, 0, 0, 0):
                        mutateChance = random.randint(1,100)
                        geneToMutate = random.randint(1,99)
                
                        color = []  
                        ran = random.randint(1,99)
                        if ran <= 33:
                            for c in range(len(rat1)):
                                color.append(rat1[c][1][0])
                                color.append(rat2[c][1][1])
                                color.append(rat2[c][1][2])
                            
                        elif ran > 33 and ran <= 66:
                            for c in range(len(rat1)):
                                color.append(rat1[c][1][1])
                                color.append(rat2[c][1][0])
                                color.append(rat2[c][1][2])

                        else:
                            for c in range(len(rat1)):
                                color.append(rat1[c][1][2])
                                color.append(rat2[c][1][0])
                                color.append(rat2[c][1][1])        
                                    
                        if mutateChance <= 30:
                                if geneToMutate <= 33:
                                    color[0] = mutate()
                                    
                                elif geneToMutate > 33 and geneToMutate <= 66:
                                    color[1] = mutate()
                                else:
                                    color[2] = mutate()             
                        if(j == 0):
                            colorRat(color, childRats[i], x, y)
                        else:
                            colorRat(color, childRats[i + len(fittestRats) // 2], x, y)
    
    return

def chooseRats():
    #choose the rats to survive
    tempRats = []
    for i in range(len(rat)):
        tempRats.append(rat[i])
    rat.clear()
    for i in range(mostFit):
        rat.append(fittestRats[i])
    for i in range(mostFit):
        rat.append(childRats[i])
    return

def select(fitness, rat):
    #select the best color for the rat
    if(fitness < 0.1):
        pasteImg(rat)
        showImg()
        quit()

def pasteImg(img):
    # Pasting img image on top of imgBack  
    # starting at coordinates (0, 0) 
    imgBack.paste(img, (0,1000), mask = img) 
    
#shows the best rat and saves it
def showImg():
    imgBack.save(r"AI Project\bestRat.jpg")
    imgBack.show()

def rateRat(rat):
    #rate the rat
    pasteImg(rat)
    showImg()
    rating = input("Please rate the rat's camo from 1-10: ")
    return rating

def addRating(rating):
    #add the rating to the rats fitness
    fittestRatsFitness[0] -= int(rating) / 10
    for x in range(len(fittestRatsFitness) - 1):
        fittestRatsFitness[x + 1] -= (int(rating) / 2) / 10
    return

#get colors of background image
colors = getPalette(imgBack)
#initialize the 1st generation of rats
for i in range(population):  
        # Get the size of the image
    width = int(rat[i].width)
    height = int(rat[i].height)
    #Process every pixel
    for x in range(width):
        for y in range(height):
            current_color = rat[i].getpixel( (x,y) )
            if current_color != (0, 0, 0, 0):
                colorRat(newColor(colors), rat[i], x, y)

#start the genetic algorithm
x = 0
for i in range(100):
    
    print("Generation: #" + str(x))
    for i in range(population):  
        fitnessArray.append(calcFitness(rat[i]))
    
    data = { 
            'Generation #' + str(x), fitnessArray[0], fitnessArray[1], fitnessArray[2], fitnessArray[3], fitnessArray[4], fitnessArray[5], fitnessArray[6]
            }   
    df = pd.DataFrame(data)
    df.to_csv('GFG.csv', mode='a', index=False, header=False)
    
    getMostFit() 
    #rating = rateRat(fittestRats[0])
    #addRating(rating)
    getMostFit() 
    fitnessArray.clear()
    if highestFitness > fittestRatsFitness[0]:
        highestFitness = fittestRatsFitness[0]
        fittestRat = fittestRats[0]
    print(highestFitness)
    select(highestFitness, fittestRats[0]) 
    crossover() 
    chooseRats() 
    x += 1

#show the best rat
pasteImg(fittestRat)
showImg()
    
    
            
    
