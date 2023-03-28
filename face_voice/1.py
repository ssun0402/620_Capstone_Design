import cv2
import face_recognition as fr
import os, sys
import numpy as np
import math
import glob
import pytesseract
import time
import threading
from multiprocessing import Process
import speech_recognition as sr
from gtts import gTTS
import playsound

r_name = []
name1 = []

def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

image_path = r'C:/Users/gptjs/OneDrive/바탕 화면/GitHub/2023-1-Capstone-/example/webcam/faces/*.png'

def face_confidence(face_distance, face_match_threshold=0.6): # face_distance 값과 face_match 임계값을 설정한 사설함수
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'

# 음성인식 시 오류나는 단어를 원하는 단어로 변경 해주는 코드
def recognition_rate(text, place, tae_eon, myung_hyun):
    for word in place + tae_eon + myung_hyun:
        if word in text:
            if word in place:
                text = text.replace(word, '620호')
            elif word in tae_eon:
                text = text.replace(word, '태언')
            elif word in myung_hyun :
                text = text.replace(word, '명현')
    return text

# 이름 인식 코드    
def speak_jetson():
            
    # 음성인식 객체 생성
    r = sr.Recognizer()
            
    with sr.Microphone() as source :
                
        # 마이크로부터 오디오 읽기
        print('"젯슨"을 불러주세요!')
        audio_data = r.record(source, duration = 3)
                
        try:
            # 구글 API로 인식 (하루에 50회 제한)
            text = r.recognize_google(audio_data, language = 'ko')
            
            # 음성인식 시 오류나는 단어
            jetson = ["잭슨", "넥슨", "넥센"]
            
            # 오류나는 젯슨 단어를 젯슨으로 바꿔주는 코드
            for i in jetson :
                if i in text :
                    text = text.replace(i, '젯슨')

            # 이름 인식 -> 음성 인식 코드로 넘어감
            if(text == "젯슨") :
                print("네! 부르셨나요?")
                txt = "네! 부르셨나요?"
                tts_kr = gTTS(txt, lang = 'ko', slow = False)
                tts_kr.save("voice.mp3")
                playsound.playsound("voice.mp3")
                return respeak()
                    
            # 다른 단어 인식 -> 다시 이름 부르는 코드로 돌아감
            else:
                return speak_jetson()
            
        # 음성 인식 실패한 경우
        except sr.UnknownValueError:
            return speak_jetson()

# 음성 인식    
def respeak():
    global r_name
    
    # 음성인식 시 오류나는 단어
    place = ['620 4', '20%', '625']
    tae_eon = ['태연', '태현']
    myung_hyun = ['명 현', '영현', '영 현', '영영', '영 영']
            
    # 음성인식 객체 생성
    r = sr.Recognizer()

    with sr.Microphone() as source :
            
        # 마이크로부터 오디오 읽기
        audio_data = r.record(source, duration = 5)
                
    try:
        # 음성을 문자열로 전환
        # 구글 API로 인식 (하루에 50회 제한)
        text = r.recognize_google(audio_data, language = 'ko')
        #테스트 후 이 위치로 변경
        #text = recognition_rate(text, place, tae_eon, myung_hyun)
        print("<음성을 문자로 변환한 값을 아래에 표시했습니다.>")
        print(text)
            
        # 오류난 단어를 원하는 단어로 변경(위치는 나중에 변경해야 함 !)
        text = recognition_rate(text, place, tae_eon, myung_hyun)
        
        # 인식된 음성에 대한 대답
        print(text + "라고 말했습니다.")
        txt = text + "라고 말했습니다."
        tts_kr = gTTS(txt, lang = 'ko', slow = False)
        tts_kr.save("voice1.mp3")
        playsound.playsound("voice1.mp3")

        # 분리할 조사
        location = ['으로', '로', '이에게', '에게', '을', '를', '이한테', '한테', '에', '이']
                
        # 문자열을 띄어쓰기 기준으로 분리
        text = text.split()
                
        # 조사가 포함된 단어를 찾은 후 조사 제거 후 리스트로 저장
        # location 단어가 포함된 단어들을 저장할 리스트
        text_division = []
                
        # 문자열을 순회하면서 location이 포함된 단어를 찾음
        for word in text :
            for loc in location :
                if loc in word :
                    # location의 단어를 제거한 후 저장
                    text_division.append(word.replace(loc, ""))
                    # 613으로 같은 경우 '으로'와 '로'가 포함되어 2번 결과가 나오게 됨
                    # break문을 통해 겹치는 단어는 표시 X
                    break
                        
        # 분리된 텍스트 중 이름 부분을 영어로 변경
        name = ['명현', '앨런', '엘런', '혜선', '희웅', '보석']
                
        for i, word in enumerate(text_division) :
            if word in name :
                if word == '희웅' :
                    text_division[i] = 'hee ung'
                    
                elif word == '명현' :
                    text_division[i] = 'myung hyun'
                    
                elif word == '혜선' :
                    text_division[i] = 'hye seon'
                    
                elif (word == '앨런') | (word == '엘런') :
                    text_division[i] = 'elon'

                elif word == '보석' :
                    text_division[i] = 'bo seok'
                    
        # 결과 출력
        print(text_division)
                
        # 분리된 텍스트 중 이름 부분을 영어로 변경
        names = ['myung hyun', 'hee ung', 'hye seon', 'elon', 'bo seok']
        place = ['613', '620', '랩실', '물건']
                
        r_name = []
        r_place = []
                
        # 결과 출력
        for i in range(len(text_division)) :
            for j in range(len(names)) :
                if names[j] == text_division[i] :
                    r_name = names[j]
                else : 
                    for x in range(len(place)) :
                        if place[x] == text_division[i] :
                            r_place = place[x]
        print('이름은', r_name)
        print('장소는', r_place)
                
        # r_name에 단어가 있으면 객체 인식 코드로 이동
        if r_name :
            return vv()
                
        else :
            return respeak()
            
    # 음성 인식 실패한 경우
    except sr.UnknownValueError:
        print("다시 한 번 말씀해주시겠어요?")
        txt = "다시 한 번 말씀해주시겠어요?"
        tts_kr = gTTS(txt, lang = 'ko', slow = False)
        tts_kr.save("voice2.mp3")
        playsound.playsound("voice2.mp3")
        return respeak()

class Facerecognition:
    face_location = []
    face_encoding = []
    face_names = []
    known_face_encoding = []
    known_face_names = []
    process_current_frame = True
    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        os.chdir('C:/Users/gptjs/OneDrive/바탕 화면/GitHub/2023-1-Capstone-/example/webcam/faces')
        file_names = os.listdir()
        for file_name in file_names :
            self.known_face_names.append(os.path.splitext(file_name)[0])
        for image in glob.glob(image_path):
            face_image = fr.load_image_file(image)
            face_encoding = fr.face_encodings(face_image)[0]
            self.known_face_encoding.append(face_encoding)
        print(self.known_face_names)
    
    def video(self):
        cap = cv2.VideoCapture(0)
        global name1
        global face_name
        if not cap.isOpened() :
            print('unable to open camera')
            sys.exit()

        while True :
            ret, frame = cap.read()
                
            if self.process_current_frame: # 인식처리를 더 빠르게 하기 위해 1/4 크기로 줄임
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                rgb_small_frame = small_frame[:, :, ::-1] # opencv의 bgr => rgb로 변경
                # gray = cv2.cvtColor(small_frame, cv2.COLOR_BGR2GRAY)
                # imgchar = pytesseract.image_to_string(gray, lang = 'eng')
                self.face_location = fr.face_locations(rgb_small_frame)
                self.face_encodings = fr.face_encodings(rgb_small_frame, self.face_location)
                self.face_names = []
                for face_encoding in self.face_encodings: # 저장된 얼굴과 캠에서 찍힌 얼굴과 비교
                    match = fr.compare_faces(self.known_face_encoding, face_encoding, 0.55)
                    face_name = "???"
                    match_percent = "??.?%"
                    face_distance = fr.face_distance(self.known_face_encoding, face_encoding) # 두 사진의 인코딩 거리 값을 비교

                    best_match_index = np.argmin(face_distance) # 최소 값을 가진 인덱스를 알려준다
                    if match[best_match_index] :
                        face_name = self.known_face_names[best_match_index]
                        match_percent = face_confidence(face_distance[best_match_index])  
                    name1 = face_name
                    self.face_names.append(f'{face_name} ({match_percent})')
            self.process_current_frame = not self.process_current_frame

            for (top, right, bottom, left), name in zip(self.face_location, self.face_names) : # 1/4로 축소된 얼굴 크기를 다시 되돌림
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 1)
                cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (0,255,0), cv2.FILLED)
                cv2.putText(frame, name, (left+ 10, bottom - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),1)

            cv2.imshow('Face Recognition', frame)
            
            global r_name
            if name1 == r_name :
                print('찾았습니다!')
                txt = "찾았습니다!"
                tts_kr = gTTS(txt, lang = 'ko', slow = False)
                tts_kr.save("voice3.mp3")
                playsound.playsound("voice3.mp3")
                
                cap.release()
                cv2.destroyAllWindows()
                
                return speak_jetson()
                
            if cv2.waitKey(1) == ord('q'):
                break
                    
        cap.release()
        cv2.destroyAllWindows()
        
def vv() :
    if __name__ == '__main__' :
        run = Facerecognition()
        run.video()

try:  
    while True :
        speak_jetson()
        respeak()
                
# Crtl + c 누르면 음성 인식 멈춤
except KeyboardInterrupt: 
    pass