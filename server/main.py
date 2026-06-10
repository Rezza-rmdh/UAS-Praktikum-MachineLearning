import os
import io
import uvicorn
import numpy as np
from numpy._typing import _32Bit
from numpy.typing import NDArray
import onnxruntime as ort
from PIL import Image
from typing import Any, cast
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(
    title = "Rice Classification API",
    description = "API for predicting rice varieties using ONNX Runtime",
    version = "1.0.0"
)

IMG_SIZE = (224, 224)
MODEL_DIR = os.path.join(os.getcwd(), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.onnx")
CLASS_NAMES = ["Arborio", "Basmati", "Ipsala", "Jasmine", "Karacadag"]

if os.path.exists(MODEL_PATH):
    session = ort.InferenceSession(MODEL_PATH, providers = ["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name
else:
    session = None
    input_name = output_name = None

def preprocess_image(image_bytes: bytes) -> NDArray[np.floating[_32Bit]]:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize(IMG_SIZE)
        image = np.array(image, dtype = np.float32)
        image = np.expand_dims(image, axis = 0)
    
        return image
    except Exception as error:
        raise HTTPException(
            status_code = 400,
            detail = f"Failed to preprocess image: {str(error)}"
        )

@app.get("/")
def home() -> dict[str, Any]:
    return {
        "message": "Rice Classification API",
        "model_path": MODEL_PATH,
        "model_loaded": session is not None
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict[str, Any]:
    try:
        if session is None:
            raise HTTPException(
                status_code = 500,
                detail = "Failed to predict: Model is not loaded"
            )
        if file.content_type is None or not file.content_type.startswith("image"):
            raise HTTPException(
                status_code = 400,
                detail = "Failed to predict: The file must be an image"
            )
    
        image_bytes = await file.read()
        image = preprocess_image(image_bytes)
        prediction = cast(np.ndarray, session.run([output_name], {input_name: image})[0])
        probabilities = prediction[0]
        predicted_idx = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_idx])
                
        return {
            "label": CLASS_NAMES[predicted_idx],
            "index": predicted_idx,
            "confidence": round(confidence * 100, 2),
            "probabilities": {
                CLASS_NAMES[i]: round(float(probabilities[i]) * 100, 2) for i in range(len(CLASS_NAMES))
            }
        }
    except Exception as error:
        raise HTTPException(
            status_code = 500,
            detail = f"Failed to predict: {str(error)}"
        )

if __name__ == "__main__":
    uvicorn.run("app:app", host = "0.0.0.0", port = 8000, reload = True)