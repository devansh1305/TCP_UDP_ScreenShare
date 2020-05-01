from PIL import ImageGrab
import numpy as np
import cv2
import tkinter as tk

root = tk.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
img = ImageGrab.grab(bbox=(0,0,width,height)) #bbox specifies specific region (bbox= x,y,width,height *starts top-left)
img_np = np.array(img) #this is the array obtained from conversion
frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
cv2.imshow("test", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()