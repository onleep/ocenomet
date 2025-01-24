import asyncio
import pickle
import re
from parser.main import apartPage

from fastapi import APIRouter, FastAPI, HTTPException

from .models import (
    FitRequest,
    List,
    MessageResponse,
    ModelList,
    Params,
    Predict,
    PredictReq,
    PredictResponse,
)
from .preprocess import encoding, prediction, prefit, preparams, prepredict, preprepict

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
        if not isinstance(data, dict): return
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
        if not request.id:
            price = prediction(data)
        else:
            price = prepredict(data, loaded_model, request.id)
            if isinstance(price, Exception):
                raise HTTPException(status_code=400, detail=str(price))
        return {'price': price}


# below are useless methods
@router.post("/fit", response_model=List[MessageResponse], status_code=201)
async def fit(request: List[FitRequest]):
    model_list = []
    for data in request:
        async with lock:
            if data.config.id in models:
                raise HTTPException(
                    status_code=422, detail=f"{data.config.id} already exist"
                )
            fitdata = prefit(
                data.X, data.y, data.config.ml_model_type, data.config.hyperparameters
            )
            if isinstance(fitdata, Exception):
                raise HTTPException(status_code=400, detail=str(fitdata))
            models[data.config.id] = pickle.dumps(fitdata)
            model_list.append(
                {'message': f"Model '{data.config.id}' trained and saved"}
            )
    return model_list


@router.post('/load', response_model=List[MessageResponse])
async def load_model(id: str):
    async with lock:
        if id not in models:
            raise HTTPException(status_code=422, detail=f'{id} not found')
        loaded_model[id] = pickle.loads(models[id])
        return [{'message': f"Model '{id}' loaded"}]


@router.post('/unload', response_model=List[MessageResponse])
async def unload():
    async with lock:
        lists = loaded_model.copy()
        loaded_model.clear()
        model_list = []
        for name in lists.keys():
            model_list.append({'message': f"Model '{name}' unloaded"})
        if not model_list:
            model_list.append({'message': 'No model to unload'})
        return model_list


@router.get('/list_models', response_model=List[ModelList])
async def list_models():
    async with lock:
        models_list = []
        for model_id, model_params in models.items():
            model_params = pickle.loads(model_params)
            model_params['model'] = str(model_params['model'])
            model_params['target_encoder'] = str(model_params['target_encoder'])
            models_list.append({"id": model_id, "params": model_params})
        if not models_list:
            models_list = [{'info': 'No model fitted'}]
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
        if not model_list:
            model_list.append({'message': 'No model to remove'})
        return model_list


app.include_router(router, prefix='/api')
