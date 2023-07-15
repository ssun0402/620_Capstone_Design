import speech_recognition as sr
from gtts import gTTS
import playsound
import os
from hangul_romanize import Transliter
from hangul_romanize.rule import academic

def check_face() : 
    print("카메라를 바라봐 주세요")
    txt = "카메라를 바라봐 주세요"
    tts_kr = gTTS(txt, lang = 'ko', slow = False)
    wav_path = os.path.join("/home/hyeun/ssun/620_capstone", "camera.wav")
    tts_kr.save(wav_path)
    playsound.playsound(wav_path)