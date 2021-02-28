from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
import uvicorn
import numpy as np
import os

from min_tfs_client.requests import TensorServingClient
from min_tfs_client.tensors import tensor_proto_to_ndarray


def read_convert_image(file):
    loaded_image = Image.open(BytesIO(file))
    image_to_convert = np.asarray(loaded_image.resize((150, 150)))[..., :3]
    image_to_convert = np.expand_dims(image_to_convert, 0)
    image_to_convert = image_to_convert / 255.0
    return np.float32(image_to_convert)


def predict(input_image):
    client = TensorServingClient(host=os.getenv("SERVING_SERVICE", "127.0.0.1"), port=8500, credentials=None)
    response = client.predict_request(
        model_name="saved_model",
        model_version=1,
        input_dict={
            "conv2d_4_input": input_image
        })

    float_output = tensor_proto_to_ndarray(
        response.outputs["dense_3"]
    )

    mapping = {
        '0': 'Cassava Bacterial Blight (CBB)',
        '1': 'Cassava Brown Streak Disease (CBSD)',
        '2': 'Cassava Green Mottle (CGM)',
        '3': 'Cassava Mosaic Disease (CMD)',
        '4': 'Healthy'}

    return mapping[str(np.argmax(float_output[0]))]


app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://ui.service.localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict/image")
async def image(image_to_predict: UploadFile = File(...)):
    if image_to_predict is None or image_to_predict.file is None:
        raise HTTPException(status_code=400, detail="Please provide an image when calling this request")

    extension = image_to_predict.filename.split(".")[-1] in ("jpg", "jpeg", "png")
    if not extension:
        raise HTTPException(status_code=400, detail="Please provide an jpg or png image")

    image_data = read_convert_image(image_to_predict.file.read())
    prediction = predict(image_data)

    return {"prediction": prediction}

@app.get('/')
async def hello():
    return {"hello": "hello"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, access_log=True)
