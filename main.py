from PIL import Image, ImageDraw, ImageFont
import random
import os
import time
import string


def generateRandomString(setOfLetters, lenght):
    return ''.join(random.choice(setOfLetters) for i in range(lenght))


def generateText(img, textString):
    
    d = ImageDraw.Draw(img)

    pos = [textPosition[0], textPosition[1]]
    
    for c in textString:
        
        selectedFontIndex = random.randint(0, len(fnt) - 1)
        selectedFont = fnt[selectedFontIndex]
        
        if debug: print(c + ' | ' + fontFileList[selectedFontIndex])

        if textRandomColor:
            charColor = generateRandomColor()
        else:
            charColor = mainColor
        
        d.text((pos[0], pos[1]), c, font = selectedFont, fill = charColor)

        charSize = d.textsize(c, font = selectedFont)
        pos[0] += charSize[0] * fontSpacing
        pos[1] = textPosition[1] + random.randint(-fontVerticalDivergence, fontVerticalDivergence)


def generateRandomCoordinates():
    return (random.randint(0, width), random.randint(0, height))

def generateRandomColor():
    if theme == 'DARK':
        vMin = 128
        vMax = 255
    elif theme == 'LIGHT':
        vMin = 0
        vMax = 128
    else:
        vMin = 0
        vMax = 255
        
    return (random.randint(vMin, vMax), random.randint(vMin, vMax), random.randint(vMin, vMax))


def generateRandomLines(img):
    d = ImageDraw.Draw(img)
    numberOfLines = random.randint(linesCountMin, linesCountMax)
    for i in range(numberOfLines):
        p1 = generateRandomCoordinates()
        p2 = generateRandomCoordinates()
        lineWidth = random.randint(linesWidthMin, linesWidthMax)
        if linesRandomColor:
            color = generateRandomColor()
        else:
            color = mainColor
        d.line([p1, p2], fill = color, width = lineWidth)

def generateRandomPoints(img):
    d = ImageDraw.Draw(img)
    numberOfPoints = random.randint(pointsCountMin, pointsCountMax)
    for i in range(numberOfPoints):
        p1 = generateRandomCoordinates()
        p2 = (p1[0] + random.randint(pointsSizeMin, pointsSizeMax), p1[1] + random.randint(pointsSizeMin, pointsSizeMax))
        if linesRandomColor:
            color = generateRandomColor()
        else:
            color = mainColor
        d.rectangle([p1, p2], fill = color)







# CONFIG

availableThemes = ['DARK', 'LIGHT', 'NONE']

# LIGHT theme will use color values superior to 128 for the R, G, and B channels
# DARK theme will use color values bellow 128.
# NONE will use the entire spectrum.
theme = availableThemes[2]

width = 400                             # Width of the resulting output
height = 300                            # Height of the resulting output

textLenght = 5                          # Lenght of the captcha
textPosition = [15, 80]                 # Starting position (x, y)
textLetters = "0123456789"              # Set of letters. Can be any string

mainColor = (0, 0, 0)                   # This is the color of the lines, points, and text
textRandomColor = False                 # If True, use random colors for each character

backgroundTransparent = False           # If True, the file will be exported in .png wihthout compression.
backgroundColor = (255, 255, 255)       # The color used in the background.

fontFolder = "font/"                    # Where are the font located
fontSizeMin = 90                        # Minimum size for the characters
fontSizeMax = 110                       # Maximum size for the characters
fontSpacing = 0.8                       # Seperation factor. 1 = no overlaying and no seperation.
fontVerticalDivergence = 30             # How much the characters's vertical position can vary.

linesEnabled = True                     # Creates random lines on the captcha
linesRandomColor = False                # If True, use random colors for each line
linesCountMin = 3                       # Minimum amount of lines
linesCountMax = 7                      # Maximum amount of lines
linesWidthMin = 2                       # Minimum thickness for the lines
linesWidthMax = 4                       # Maximum thickness for the lines

pointsEnabled = True                    # Creates random points on the captcha
pointsRandomColor = False               # If True, use random colors for each point
pointsCountMin = 400                    # Minimum amount of points
pointsCountMax = 1000                   # Maximum amount of points
pointsSizeMin = 2                       # Minimum size of a point
pointsSizeMax = 4                       # Maximum size of a point

exportFolder = 'output/'                # The folder path for the export folder.
exportCount = 1000                       # The number of captcha to generate.
exportName = 'captcha'                  # A number will be appended if exportCount > 1
jpgQuality = 0                          # The quality of the exportation. Only compatible with JPG

# Displays debug messages in the console.
# Will display which font have been imported,
# which font has been used for each character.
# That can be useful when testing new fonts.
debug = False


# END CONFIG









# Create the folders if they don't exist.
if not os.path.exists(fontFolder):
    if debug: print('\nThe font folder is missing. Trying to create a folder at this path: ' + fontFolder)
    os.mkdir(fontFolder)
    if debug: print('The font folder has been created successfully.')
if not os.path.exists(exportFolder):
    if debug: print('\nThe export Folder is missing. Trying to create a folder at this path: ' + exportFolder)
    os.mkdir(exportFolder)
    if debug: print('The export Folder has been created successfully.')


# Get the list of font in the font folder
fnt = []
fontFileList = os.listdir(fontFolder)

if debug: print('\n\nIMPORTING THE FONT FROM THIS FOLDER: ' + fontFolder + '\n')
for filepath in fontFileList:
    filename, file_extension = os.path.splitext(filepath)

    # Only otf and ttf files are accepted, regardless of upper or lowercase
    if file_extension.lower() == '.otf' or file_extension.lower() == '.ttf':
        fontSize = random.randint(fontSizeMin, fontSizeMax)
        fnt += [ImageFont.truetype(fontFolder + filename + file_extension, fontSize)]
        if debug: print(filename + file_extension + ' has been imported.')

    elif debug:
        print(fontFolder + filename + file_extension + ' is not a valid font file. Skipping it.')

# If no font was imported, aborts.
if len(fnt) == 0:
    print('ERROR: No font present. Please add fonts (.ttf or .otf files) to the correct folder : ' + fontFolder)
    exit(1)


# Now generate exportCount captcha(s)
for i in range(exportCount):
    
    if debug: print('')

    # Create the base image with the proper background
    if backgroundTransparent:
        img = Image.new('RGBA', (width, height))
    else:
        img = Image.new('RGB', (width, height), color = backgroundColor)
    text = generateRandomString(textLetters, textLenght)
    # Generation
    generateText(img, text)
    if linesEnabled:  generateRandomLines(img)
    if pointsEnabled: generateRandomPoints(img)

    # Exportation
    outputName = exportFolder + text
    if exportCount > 1: outputName +=  '_' + str(i)
    if backgroundTransparent:
        outputName += '.png'
    else:
        outputName += '.jpg'

    img.save(outputName, quality = jpgQuality)    
    if debug: print('The captcha above has been saved as ' + outputName + '\n')

    

    
