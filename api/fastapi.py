from .preprocess import preparams, preprepict, encoding, prediction
from fastapi import FastAPI, HTTPException
from app.main import apartPage
from .models import *
import uvicorn
import re

app = FastAPI()


@app.get('/getparams', response_model=Predict)
async def getparams(url: str):
    match = re.search(r'flat/(\d{4,})', url)
    if not match or not (id := match.group(1)):
        raise HTTPException(status_code=400, detail=f'Неверный формат объявления')
    data = apartPage([id], dbinsert=0)
    data = Params(**data)
    response = preparams(data)
    return response


@app.get('/predict', response_model=PredictResponse)
async def predict(request: Predict):
    data = preprepict(request)
    data_enc = encoding(data)
    price = prediction(data_enc)
    return {'price': price}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
