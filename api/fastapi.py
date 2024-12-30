from .models import Predict, Params, PredictResponse, PredictReq, MessageResponse, FitRequest, LoadRequest, ModelList
from .preprocess import preparams, preprepict, encoding, prediction
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from fastapi import FastAPI, HTTPException, APIRouter
from sklearn.preprocessing import TargetEncoder
from app.main import apartPage
from app.tools import logging
from typing import List
import pandas as pd
import uvicorn
import asyncio
import pickle
import re

app = FastAPI()
router = APIRouter()


models = {}
loaded_model = {}
lock = asyncio.Lock()


@router.get('/getparams', response_model=Predict)
async def getparams(url: str):
    async with lock:
        match = re.search(r'flat/(\d{4,})', url)
        if not match or not (id := match.group(1)):
            raise HTTPException(status_code=400, detail='Неверный формат объявления')
        data = apartPage([id], dbinsert=0)
        if not data:
            raise HTTPException(status_code=400, detail='Неверный формат объявления')
        data = Params(**data)
        response = preparams(data)
        return response


@router.post('/predict', response_model=PredictResponse)
async def predict(request: PredictReq):
    async with lock:
        data = preprepict(request.data)
        if not request.id:
            data = encoding(data)
        if isinstance(data, ValueError):
            raise HTTPException(status_code=400, detail=str(data))
        if not request.id: price = prediction(data)
        else:
            target_columns = data.select_dtypes(exclude=['number', 'boolean']).columns
            data[target_columns] = pd.DataFrame(loaded_model[request.id]['target_encoder'].transform(
                data[target_columns]), columns=target_columns)
            price = await asyncio.to_thread(loaded_model[request.id]['model'].predict, data)
        return {'price': price}

# below are useless methods
@router.post('/fit', response_model=List[MessageResponse], status_code=201)
async def fit(request: List[FitRequest]):
    model_list = []
    for data in request:
        async with lock:
            if data.config.id in models:
                raise HTTPException(status_code=422, detail=f'{data.config.id} already exist')
            if data.config.ml_model_type == 'lr':
                model = LinearRegression(**data.config.hyperparameters)
            elif data.config.ml_model_type == 'ls':
                model = Lasso(**data.config.hyperparameters)
            else:
                model = Ridge(**data.config.hyperparameters)

            target_encoder = TargetEncoder(target_type='continuous')
            df = pd.DataFrame(data.X)
            y = pd.DataFrame(data.y)
            cols = df.select_dtypes(exclude=['number', 'boolean']).columns
            df[cols] = pd.DataFrame(target_encoder.fit_transform(
                df[cols], data.y), columns=cols)
            model.fit(df, y)
            models[data.config.id] = pickle.dumps({
                'model': model,
                'target_encoder': target_encoder})
            model_list.append({'message': f"Model '{data.config.id}' trained and saved"})
    return model_list


@router.post('/load', response_model=List[MessageResponse])
async def load_model(request: LoadRequest):
    async with lock:
        if request.id not in models:
            raise HTTPException(status_code=422, detail=f'{request.id} not found')
        loaded_model[request.id] = pickle.loads(models[request.id])
        return [{'message': f"Model '{request.id}' loaded"}]


@router.post('/unload', response_model=List[MessageResponse])
async def unload():
    async with lock:
        lists = loaded_model.copy()
        loaded_model.clear()
        model_list = []
        for name in lists.keys():
            model_list.append({'message': f"Model '{name}' unloaded"})
        if not model_list: model_list.append({'message': 'No model to unload'})
        return model_list


@router.get('/list_models', response_model=List[ModelList])
async def list_models():
    async with lock:
        models_list = []
        for model_id, model_data in models.items():
            model = pickle.loads(model_data)['model']
            if isinstance(model, LinearRegression):
                model_type = 'lr'
            elif isinstance(model, Lasso):
                model_type = 'ls'
            elif isinstance(model, Ridge):
                model_type = 'rg'
            else: continue
            models_list.append({
                "id": model_id,
                "type": model_type})

        if not models_list: models_list = [{'info': 'No model fitted'}]
        return [{"models": models_list}]


@router.delete('/remove/{model_id}', response_model=List[MessageResponse])
async def remove(model_id: str):
    async with lock:
        if model_id not in models:
            raise HTTPException(status_code=422, detail=f'{model_id} not found')
        del models[model_id]
        return [{'message': f"Model '{model_id}' removed"}]


@router.delete('/remove_all', response_model=List[MessageResponse])
async def remove_all():
    async with lock:
        lists = models.copy()
        models.clear()
        model_list = []
        for name in lists.keys():
            model_list.append({'message': f"Model '{name}' removed"})
        if not model_list: model_list.append({'message': 'No model to remove'})
        return model_list

app.include_router(router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
