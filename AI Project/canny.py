import cv2 
  
img = cv2.imread(r"C:\Users\rude3\Documents\GitHub\AI_Rat_Project\AI Project\img1.jpg")  # Read image 
cv2.resize(img, (400, 543))
# Setting parameter values 
t_lower = 50  # Lower Threshold 
t_upper = 150  # Upper threshold 
  
# Applying the Canny Edge filter 
edge = cv2.Canny(img, t_lower, t_upper) 
cv2.namedWindow('original', cv2.WINDOW_NORMAL)
cv2.resizeWindow('original', 400, 543)

cv2.imshow('original', img) 

cv2.namedWindow('edge', cv2.WINDOW_NORMAL)
cv2.resizeWindow('edge', 400, 543)

cv2.imshow('edge', edge) 
cv2.resizeWindow('edge', (400,543))

cv2.waitKey(0) 
cv2.destroyAllWindows() 