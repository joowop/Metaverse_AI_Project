from fastapi import FastAPI , File, UploadFile
from fastapi.responses import FileResponse
import shutil
from torchvision import datasets, models, transforms
import torch
from PIL import Image

from routers.chat import chatbot

app = FastAPI()
app.include_router(chatbot)

model = torch.load('model/model (1).pt',map_location=torch.device('cpu'))
model.to('cpu')

@app.get('/')
def root():
    return {"message":"Hello~~~"}

@app.post('/sendimg')
def sendimg(file:UploadFile=File(...)):
    print(file.filename)
    path = f'files/{file.filename}'
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(file.file, buffer)

    transforms_test = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406],[0.229,0.224,0.225])
    ])

    image = Image.open(f'files/{file.filename}')
    image = transforms_test(image).unsqueeze(0).to('cpu')

    classname = ['마동석','이국주','카리나']

    with torch.no_grad():
        outputs = model(image)
        _,preds = torch.max(outputs,1)
        print(outputs)
        print(classname[preds[0]])

    return {'result':classname[preds[0]]}

    return {"message":"OK"}