import speech_recognition as sr
from gtts import gTTS
import playsound
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import random
import numpy as np
import pandas as pd

# 리얼한 목소리 : https://guide.ncloud-docs.com/docs/ko/naveropenapiv3-speech-clovavoice

# 한국어 모델 불러오기
model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')
df1 = pd.read_csv('embeding.csv',header=None)
df = pd.read_csv('ChatbotData.csv')
# 유사도 구하기
def chatbot_text(text):
    em_result = model.encode(text)

    co_result = []
    for temp in range(len(df1)):
        data = df1.iloc[temp]
        co_result.append(cosine_similarity([data],[em_result])[0][0])

    df['cos'] = co_result
    df_result = df.sort_values('cos',ascending=False)
    r = random.randint(0,5)

    return df_result.iloc[r]['A']

# 더 현실적인 아웃풋 음성을 내기 위한 네이버 코드
def naver():
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"

    encText = urllib.parse.quote("반갑습니다 네이버")
    data = "speaker=mijin&speed=0&text=" + encText

    url = "https://openapi.naver.com/v1/voice/tts.bin"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()

    if (rescode == 200):
        print("TTS mp3 저장")
        response_body = response.read()
        with open('1111.mp3', 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)


# tts = gTTS(text='안녕하세요 인공지능반에 오신걸 환영합니다.')
# tts.save('test.mp3')
# time.sleep(1)
# playsound.playsound('test.mp3')

try:
    while True:

        r = sr.Recognizer()

        with sr.Microphone() as source:
            print('음성을 입력하세요')
            audio = r.listen(source)

            try:
                result = r.recognize_google(audio, language='ko-KR')
                print('음성 : ' + result)
                chat_result = chatbot_text(result)

                print('응답 : ' + chat_result)

                tts = gTTS(text=chat_result)
                tts.save('chat.mp3')
                time.sleep(1)
                playsound.playsound(tts)
                # playsound.playsound('chat.mp3')

            except sr.UnknownValueError:
                print('다시 입력해주세요')
            except:
                print('알수 없는 오류')
except:
    pass