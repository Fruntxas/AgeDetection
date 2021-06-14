from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras import models
import numpy as np
from api.utils_basic import image_to_array, convert_weight, age_range, weighted_accuracy, predict

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

model_path = 'models/best_model'
model = models.load_model(model_path)


# Upload Image
@app.post("/image")
async def read_root(file: UploadFile = File(...)):

    with open("tmp.jpg", "wb+") as data:
        data.write(file.file.read())
        print("Written to image")

    print(f"Import file type is {type(file.file)}")

    # Converting Image to Array and Scaling
    X = image_to_array("tmp.jpg")
    
    # Exception created
    if X[0] != 100:
        return {"No Face detected": "No Face detected"}
    
    X = X/255 - 0.5
    print("Scaled Image converted to array")

    # Predicting
    y_pred = predict(model, X)  # [0]
    print(y_pred)
    print("Prediction Performed")

    #Main Bin
    main_pred = np.argmax(y_pred)

    # Pred List for weighted prediction
    weighted_pred = weighted_accuracy(y_pred)
    print(weighted_pred)

    output = {"Age Bin": age_range(int(weighted_pred)), "Weighted Guess": int(weighted_pred*5+1)}
    print("Guesses Performed")

    return output


@app.get("/")
def index():
    return {"Greetings": "Welcome to the Age Prediction"}
