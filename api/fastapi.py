from fastapi import FastAPI, Request, HTTPException
from preprocess import preprocess
import uvicorn
import json

app = FastAPI()


@app.post('/predict')
async def process_json(request: Request):
    contents = await request.body()
    data = json.loads(contents)
    X = preprocess(data)
    if isinstance(X, list): 
        raise HTTPException(status_code=400, detail=f'В объявлении не указаны: {X}')
    response = {'X': X.to_json(orient='records', force_ascii=False)}
    return {'message': 'IZI', 'X_data': response}


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)
