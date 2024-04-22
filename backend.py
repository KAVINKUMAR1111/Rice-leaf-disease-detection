from io import BytesIO
import tensorflow as tf
import numpy as np
from PIL import Image
from fastapi import FastAPI, File, UploadFile

app = FastAPI()
model = tf.keras.models.load_model('ml_model.h5')
CLASS_NAMES = ['Bacterial leaf blight', 'Brown spot', 'Healthy', 'Hispa', 'Leaf smut', 'LeafBlast']

def read_file_as_image(data) -> np.ndarray:
    img = Image.open(BytesIO(data)).convert('RGB')
    img = img.resize((224, 224))
    image = np.array(img)
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    predictions = np.array(model.predict(img_batch))
    predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = float(np.max(predictions[0]))
    return {
        'class': predicted_class,
        'confidence': confidence
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='localhost', port=8009)
