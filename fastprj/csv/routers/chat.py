import numpy as np
from fastapi import APIRouter
from fastapi import Form
from typing_extensions import Annotated
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import random

np.set_printoptions(precision=6, suppress=True)
chatbot = APIRouter(prefix='/chat')

model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
model = model.to('cpu')
df = pd.read_csv('./csv/ChatBotData.csv')
df1 = pd.read_csv('./csv/embeding.csv',header=None)

def chatbot_text(text):
    em_result = model.encode(text)
    co_result = []
    for temp in range(len(df1)):
        data = df1.iloc[temp]
        co_result.append(cosine_similarity([em_result],[data])[0][0])
    df['cos'] = co_result
    df_result = df.sort_values('cos',ascending=False)
    r = random.randint(0,5)
    return df_result.iloc[r]



@chatbot.get('/send',tags=['chat'])
def sendchat():
    return {'chat':'안녕'}

@chatbot.post('/send',tags=['chat'])
def sendchat_post(text:Annotated[str, Form()]):
    print(text)
    result = chatbot_text(text)
    return {'chat':result.A}