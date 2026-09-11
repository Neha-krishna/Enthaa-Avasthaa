import numpy as np
from PIL import Image

def calculate_meltdown(image,temperature,humidity,sun_exposure):
    temperature=max(0,min(50,temperature)); humidity=max(0,min(100,humidity)); sun_exposure=max(0,min(100,sun_exposure))
    brightness=float(np.array(image).mean())/255*100
    heat=max(0,temperature-10)/40*100
    risk=max(0,min(100,heat*.58+humidity*.12+sun_exposure*.25+brightness*.05))
    seconds=int(max(18,900-risk*8.2))
    if risk<25: level,msg="CALM","Your ice cream is currently pretending to be stable."
    elif risk<50: level,msg="WARMING UP","The scoop has entered a questionable phase."
    elif risk<75: level,msg="MELTDOWN WARNING","Ice cream soup formation is becoming increasingly likely."
    else: level,msg="TOTAL MELTDOWN","Eat it immediately. Science has lost control."
    return {"meltdown_risk":round(risk,1),"disaster_level":level,"estimated_stability_seconds":seconds,"temperature":round(temperature,1),"humidity":round(humidity,1),"sun_exposure":round(sun_exposure,1),"brightness":round(brightness,1),"message":msg,"note":"Playful demo estimate, not a scientific melting-time prediction."}
