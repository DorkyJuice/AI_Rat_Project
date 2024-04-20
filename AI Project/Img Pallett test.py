
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
#rat generations
rat = []
#children of the fit rats
childRats = []
#fitness of the rats
fitnessArray = []
#fittest half of the generation of rats
fittestRats = []
#fitness of the fittest rats
fittestRatsFitness = []
#initial population size
population = 100
#number of the most fit rats we pull from the population
mostFit = population // 2
#if it should mutate more (explore)
moreMutation = False
#counter for mutation chance in generation
whenMoreMutation = 0

for x in range(population):
    # Opening the secondary image (Rat overlay image) 
    rat.append(Image.open(r"AI Project/Rat.png"))
#fitness value of the most fit rat
highestFitness = 1
#most fit rat
fittestRat = Image.open(r"AI Project/Rat.png")
#gets pallet of background image
def getPalette(img):
    color_count = []
    reduced = img.convert("P", palette=Image.Palette.WEB) # convert to web palette (216 colors)
    palette = reduced.getpalette() # get palette as [r,g,b,r,g,b,...]
    palette = [palette[3*n:3*n+3] for n in range(256)] # group 3 by 3 = [[r,g,b],[r,g,b],...]
    color_count = [(n, palette[m]) for n,m in reduced.getcolors()]
    color_count.sort(reverse=True) #sort color frequency in descending order
    for i in range(len(color_count)):
        if color_count[i][1] == (0,0,0):
            color_count.pop(i)
            break
    return color_count
#grabs a random color from the background image or parents
def newColor(color_count):
    new_color = color_count[random.randint(0, len(color_count)-50)][1]
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
     image1_lab = image1_lab.tolist()
     image2_lab = image2_lab.tolist()
#     #get the difference of the lab values between the 2 images
     delta_E = colour.delta_E(image1_lab, image2_lab)
#     #get the mean of the difference
     mean = float(np.mean(delta_E))
     #calculate fitness value of color difference
     fitness = mean / 100

     #print(fitness)
     
     return fitness

#finds the difference in color between the each color in the rat and the background and uses that as the fitness value  
def calcColorFitness(color):
    colorFitnessArray = 0
        
#     #save the crop and recolored rat
    imgBackcrop.save(r"AI Project\Temp\crop.jpg")
#     #open them in cv2 (might change this down the line if it takes to long)
    image1_rgb = cv2.imread(r"AI Project\Temp\crop.jpg")
    color_rgb = np.array([[color]])
#     #convert the RGB values to lab
    image1_lab = cv2.cvtColor(image1_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
    color_lab = cv2.cvtColor(color_rgb.astype(np.float32) / 255, cv2.COLOR_RGB2Lab)
    image1_lab = image1_lab.tolist()
#     #get the difference of the lab values between the 2 images
    delta_E = colour.delta_E(image1_lab, color_lab)
#     #get the mean of the difference
    mean = float(np.mean(delta_E))
    #calculate fitness value of color difference
    colorFitnessArray = (mean / 100) + color[2] - color[0]# + (color[1] // 2)
     
    return colorFitnessArray
 
#finds the most fit rat in the population
def getMostFit():
    #initialize variables
    fittestRats.clear()
    fittestRatsFitness.clear()
    tempRats = []
    tempFitness = []
    #fill temp variables with the current population and fitness values
    for i in range(len(rat)):
        tempRats.append(rat[i])
    for i in range(len(fitnessArray)):
        tempFitness.append(fitnessArray[i])
    
    #initialize best rat and index
    tempBest = tempFitness[0]
    tempBestIndex = 0
    #find the most fit rats in the population
    for x in range(mostFit):
        for y in range(len(tempFitness)):
            if(tempBest > tempFitness[y]):
                tempBest = tempFitness[y]
                tempBestIndex = y
        #sort them by fitness    
        fittestRats.append(rat[tempBestIndex])
        fittestRatsFitness.append(tempFitness[tempBestIndex])
        tempRats.pop(tempBestIndex)
        tempFitness.pop(tempBestIndex)
        tempBest = tempFitness[0]
        tempBestIndex = 0

#finds the most fit color in the population
def getColorMostFit(colors, cFitness):
    #check if its being more exploratory or exploitative
    if moreMutation == True:
        mostFitColors = (len(colors) // 3) * 2
    else:
        mostFitColors = len(colors) // 2
    #initialize variables
    tempRatColor = []
    tempRatColorFitness = []
    #fill temp variables with the current population of colors and fitness values
    for i in range(len(colors)):
        tempRatColor.append(colors[i])
    for i in range(len(cFitness)):
        tempRatColorFitness.append(cFitness[i])
    #clear initial variables
    colors.clear()
    cFitness.clear()
    #set temp best and index
    tempBest = 1
    tempBestIndex = 0
    #find the most fit colors in the population
    for x in range(mostFitColors):
        for y in range(len(tempRatColorFitness)):
            if(tempBest > tempRatColorFitness[y]):
                tempBest = tempRatColorFitness[y]
                tempBestIndex = y
        if(len(tempRatColor) == 0):
            break 
        #sort them by fitness
        colors.append(tempRatColor[tempBestIndex])
        cFitness.append(tempRatColorFitness[tempBestIndex])
        tempRatColor.pop(tempBestIndex)
        tempRatColorFitness.pop(tempBestIndex)
        tempBest = 1
        tempBestIndex = 0
    return colors
        

def mutate():
    #mutate the color of the rat
    return random.randint(0,255)

def crossover():
    #crossover the color of the rat
    for j in range(2):
        for i in range(len(fittestRats) - len(fittestRats) // 2): 
            #initialize variables
            rat1 = list(getPalette(fittestRats[i]))
            rat2 = list(getPalette(fittestRats[i + len(fittestRats) // 2]))
            rat1Fit = []
            rat2Fit = []
            #get the fitness of the colors
            for p in range(len(rat1)):
                if(rat1[p][1] != [0,0,0]):
                    rat1Fit.append(calcColorFitness(rat1[p][1]))
                else:
                    rat1Fit.append(1000) 
            for p in range(len(rat2)):    
                if(rat2[p][1] != [0,0,0]):
                    rat2Fit.append(calcColorFitness(rat2[p][1]))
                else:
                    rat2Fit.append(200)
            rat1 =  getColorMostFit(rat1, rat1Fit)
            rat2 = getColorMostFit(rat2, rat2Fit)

            #initialize the children
            childRats.append(Image.open(r"AI Project/Rat.png"))
            
            # Get the size of the image
            width = int(childRats[i].width)
            height = int(childRats[i].height)
            c = 0
            #Process every pixel
            for x in range(width):
                for y in range(height):
                    current_color = rat[i].getpixel( (x,y) )
                    #ignore the transparent pixels
                    if current_color != (0, 0, 0, 0):
                        #check if exploration or exploitation
                        if moreMutation == True:
                            mutateChance = random.randint(1,100)
                        else:
                            mutateChance = random.randint(1,1000)
                        #cross over the colors with odd numbers in c adding from rat1 and even numbers in c adding from rat2
                        if c > len(rat1) - 1 or c > len(rat2) - 1:
                            c = 0
                        if(len(rat1) <= 1 or len(rat2) <= 1):
                            c = 0
                        if j == 0:
                            if c % 2 == 1:
                                if mutateChance <= 1:
                                    colorRat([mutate(), mutate(), mutate()], childRats[i], x, y)
                                else:
                                    colorRat(rat1[random.randint(0, (len(rat1)) - 1 - c)][1], childRats[i], x, y)
                            else:
                                if mutateChance <= 1:
                                    colorRat([mutate(), mutate(), mutate()], childRats[i], x, y)
                                else:
                                    colorRat(rat2[random.randint(0, (len(rat2)) - 1 - c)][1], childRats[i], x, y)
                        else:
                            if c % 2 == 1:
                                if mutateChance <= 1:
                                    colorRat([mutate(), mutate(), mutate()], childRats[i + len(fittestRats) // 2], x, y)
                                else:
                                    colorRat(rat1[random.randint(0, (len(rat1)) - 1 - c)][1], childRats[i + len(fittestRats) // 2], x, y)
                            else:
                                if mutateChance <= 1:
                                    colorRat([mutate(), mutate(), mutate()], childRats[i + len(fittestRats) // 2], x, y)
                                else:
                                    colorRat(rat2[random.randint(0, (len(rat2)) - 1 - c)][1], childRats[i + len(fittestRats) // 2], x, y)
                        c += 1
                        
    
    return

def chooseRats():
    #choose the rats to survive
    tempRats = []
    for i in range(len(rat)):
        tempRats.append(rat[i])
    rat.clear()
    #fill new generation with the most fit rats and the children of the most fit rats
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
    #append to csv
    data = { 
            'Generation #' + str(x), fitnessArray[0], fitnessArray[1], fitnessArray[2], fitnessArray[3], fitnessArray[4], fitnessArray[5], fitnessArray[6]
            }   
    df = pd.DataFrame(data)
    df.to_csv('GFG.csv', mode='a', index=False, header=False)
    
    getMostFit() 
    fitnessArray.clear()
    #check if the most fit rat of the generation is the most fit rat of all time
    if highestFitness > fittestRatsFitness[0]:
        highestFitness = fittestRatsFitness[0]
        fittestRat = fittestRats[0]
        moreMutation = False
        whenMoreMutation = 0
        pasteImg(fittestRat)
        showImg()
    #if 5 generations pass without the most fit rat changing, make it more exploratory
    else:
        whenMoreMutation += 1
        if whenMoreMutation <= 5:
            moreMutation = False
        if whenMoreMutation > 5:
            moreMutation = True
            if whenMoreMutation == 10:
                whenMoreMutation = 0


    print(highestFitness)
    select(highestFitness, fittestRats[0]) 
    crossover() 
    chooseRats() 
    fittestRats.clear()
    fittestRatsFitness.clear()
    x += 1

#show the best rat
pasteImg(fittestRat)
showImg()
    
    
            
    
