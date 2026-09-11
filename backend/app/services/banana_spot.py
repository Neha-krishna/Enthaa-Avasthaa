import cv2, numpy as np
from PIL import Image

def analyze_banana(image:Image.Image):
    rgb=np.array(image)
    h,w=rgb.shape[:2]
    scale=min(1,900/max(h,w))
    if scale<1: rgb=cv2.resize(rgb,(int(w*scale),int(h*scale)))
    hsv=cv2.cvtColor(rgb,cv2.COLOR_RGB2HSV)
    yellow=cv2.inRange(hsv,np.array([12,45,70],np.uint8),np.array([42,255,255],np.uint8))
    dark=cv2.inRange(hsv,np.array([0,0,0],np.uint8),np.array([45,255,125],np.uint8))
    banana=cv2.dilate(yellow,np.ones((11,11),np.uint8),iterations=1)
    mask=cv2.bitwise_and(dark,banana)
    k=np.ones((5,5),np.uint8)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,k)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,k)
    contours,_=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    area=rgb.shape[0]*rgb.shape[1]
    spots=[]
    for c in contours:
        a=cv2.contourArea(c)
        if max(8,area*.000015)<=a<=area*.08:
            spots.append(a)
    spots=sorted(spots,reverse=True)[:50]
    banana_pixels=np.count_nonzero(yellow)
    density=(np.count_nonzero(mask)/banana_pixels*100) if banana_pixels else 0
    largest=spots[0] if spots else 0
    average=sum(spots)/len(spots) if spots else 0
    score=min(100,round(len(spots)*3+density*.9+min(largest/max(area,1)*1000,20),1))
    n=len(spots)
    if n<=4: personality,crisis,verdict="Suspiciously Clean","LOW","This banana is refusing to provide enough drama."
    elif n<=12: personality,crisis,verdict="Mildly Speckled","MEDIUM","The banana has started developing a personality."
    elif n<=24: personality,crisis,verdict="Spot Enthusiast","HIGH","There are enough spots to justify using AI."
    else: personality,crisis,verdict="Absolute Chaos","EXTREME","This banana has become a data science problem."
    return {"fruit":"Banana","spots_detected":n,"spot_density_percent":round(density,1),"largest_spot_pixels":round(largest,1),"average_spot_pixels":round(average,1),"spot_score":score,"spot_personality":personality,"crisis_level":crisis,"verdict":verdict,"note":"Experimental visual spot count for entertainment; not a food-safety assessment."}
