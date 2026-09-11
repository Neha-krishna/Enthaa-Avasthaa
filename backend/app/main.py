from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import io
from app.services.banana_spot import analyze_banana
from app.services.meltdown_engine import calculate_meltdown

app=FastAPI(title="FOOD CRISIS AI")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000","http://127.0.0.1:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root(): return {"message":"FOOD CRISIS AI backend is running"}

@app.get("/api/health")
def health(): return {"status":"ok"}

@app.post("/api/analyze-banana")
async def banana(file: UploadFile=File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400,"Please upload an image.")
    try: return analyze_banana(Image.open(io.BytesIO(await file.read())).convert("RGB"))
    except Exception as e: raise HTTPException(400,str(e))

@app.post("/api/analyze-icecream")
async def icecream(file: UploadFile=File(...), temperature:float=Form(28), humidity:float=Form(55), sun_exposure:float=Form(50)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400,"Please upload an image.")
    try: return calculate_meltdown(Image.open(io.BytesIO(await file.read())).convert("RGB"),float(temperature),float(humidity),float(sun_exposure))
    except Exception as e: raise HTTPException(400,str(e))
