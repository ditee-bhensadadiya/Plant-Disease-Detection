from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf  

app = FastAPI()

origins = [
    "http://localhost:8000", 
    "http://127.0.0.1:8000",  
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load model 
model = tf.keras.models.load_model("C:\\Users\\ditib\\Desktop\\Plant Disease Detection\\saved_model\\models\\model1\\1\\1.keras")
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]
    
@app.get("/ping")
async def ping():
    return "Hello, I am alive"

# Helper function to process the image
def read_file_as_image(data) -> np.ndarray:
    image = Image.open(BytesIO(data)).convert("RGB")
    image = image.resize((224, 224))  
    image = np.array(image) / 255.0  
    return image

# Predict endpoint
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Read and process the file
        image = read_file_as_image(await file.read())
        img_batch = np.expand_dims(image, 0)

        # Make a prediction
        prediction = model.predict(img_batch)

        # Return results
        predicted_class = CLASS_NAMES[np.argmax(prediction)]
        confidence = np.max(prediction)
        return {"class": predicted_class, "confidence": float(confidence)}
    except Exception as e:
        return {"error": f"Failed to process the request: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=8001)
