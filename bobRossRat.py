from PIL import Image
#Opening the primary image (used in background)
img1 = Image.open(r"C:\Users\jessb\OneDrive\Desktop\AI\distant_moutains.jpg") 
#Opening the secondary image (overlay image)
img2 = Image.open(r"C:\Users\jessb\OneDrive\Desktop\AI\distant_moutains.jpg") 
#Pasting img2 image on top of img1
#starting at coordinates (0, 0)
img1.paste(img2, (0,1000), mask = img2)