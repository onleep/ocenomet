from fastapi import FastAPI, HTTPException
from .preprocess import preparams, preprocess
from app.main import apartPage
from .models import *
import pandas as pd
import uvicorn
import pickle
import re

app = FastAPI()

with open('model.pickle', 'rb') as file:
    model_data = pickle.load(file)

model = model_data['model']
onehot_encoder = model_data['onehot_encoder']
target_encoder = model_data['target_encoder']
scaler = model_data['scaler']


@app.get('/getparams')
async def getparams(url: str):
    match = re.search(r'flat/(\d{4,})', url)
    if not match or not (id := match.group(1)):
        raise HTTPException(status_code=400, detail=f'Неверный формат объявления')
    data = apartPage([id], dbinsert=0)
    data = Data(**data)
    response = preparams(data)
    return response.iloc[0].to_json(force_ascii=False)


@app.get('/predict')
async def predict(request: dict):
    return {'price': 66669999.00}

    X_train = preprocess(request)
    if isinstance(X_train, list):
        raise HTTPException(status_code=400, detail=f'В объявлении не указаны: {X}')
    return X_train.iloc[0].to_json(force_ascii=False)
    onehot_columns = ['county', 'flat_type', 'sale_type',
                      'category', 'material_type', 'travel_type']
    X_train_encoded = pd.DataFrame(onehot_encoder.transform(
        X_train[onehot_columns]), columns=onehot_encoder.get_feature_names_out(onehot_columns))
    X_train = pd.concat([X_train.drop(columns=onehot_columns).reset_index(
        drop=True), X_train_encoded], axis=1)

    ordinal_columns = {'repair_type': {'no': 0, 'cosmetic': 1, 'euro': 2, 'design': 3}}
    for col, mapping in ordinal_columns.items():
        X_train[col] = X_train[col].map(mapping)

    target_columns = ['district', 'project_type', 'metro']
    X_train[target_columns] = pd.DataFrame(target_encoder.transform(
        X_train[target_columns]), columns=target_columns)
    return X_train.to_json()
    # Scaler
    # X_train = pd.DataFrame(scaler.transform(X_train), columns=X_train.columns)

    pred = model.predict(X_train)
    return {"message": 'IZI', "X_data": pred}


if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)
