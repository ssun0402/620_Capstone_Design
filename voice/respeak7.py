# 재확인 코드

import speech_recognition as sr
from gtts import gTTS
import playsound

# 음성인식 시 오류나는 단어를 원하는 단어로 변경 해주는 코드
def recognition_rate(text, place, tae_eon, myung_hyun):
    for word in place + tae_eon + myung_hyun:
        if word in text:
            if word in place:
                text = text.replace(word, '620')
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
                tts_kr.save("voice.wav")
                playsound.playsound("voice.wav")
                return respeak()
            
            # 다른 단어 인식 -> 다시 이름 부르는 코드로 돌아감
            else:
                return speak_jetson()
            
        # 음성 인식 실패한 경우
        except sr.UnknownValueError:
            return speak_jetson()

# 음성 인식    
def respeak():
    # 음성인식 시 오류나는 단어
    place = ['620 4']
    tae_eon = ['태연', '태현']
    myung_hyun = ['명 현', '영현', '영 현']
    
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
        print(text + "라고 말했습니까?")
        txt = text + "라고 말했습니까?"
        tts_kr = gTTS(txt, lang = 'ko', slow = False)
        tts_kr.save("voice.wav")
        playsound.playsound("voice.wav")
        
        # 이 부분 수정 해야 함!
        # 마이크로부터 오디오 읽기
        audio_data = r.record(source, duration = 5)
        text1 = r.recognize_google(audio_data, language = 'ko')

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
        name = ['명현', '태언', '혜선', '희웅']
        
        for i, word in enumerate(text_division) :
            if word in name :
                if word == '희웅' :
                    text_division[i] = 'hee ung'
            
                elif word == '명현' :
                    text_division[i] = 'myung hyun'
            
                elif word == '혜선' :
                    text_division[i] = 'hye seon'
            
                elif word == '태언' :
                    text_division[i] = 'tae eon'
            
        # 결과 출력
        print(text_division)
        
        # 분리된 텍스트 중 이름 부분을 영어로 변경
        names = ['myung hyun', 'hee ung', 'hye seon', 'tae eon']
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
        
        return speak_jetson()
    
    # 음성 인식 실패한 경우
    except sr.UnknownValueError:
        print("다시 한 번 말씀해주시겠어요?")
        txt = "다시 한 번 말씀해주시겠어요?"
        tts_kr = gTTS(txt, lang = 'ko', slow = False)
        tts_kr.save("voice.wav")
        playsound.playsound("voice.wav")
        return respeak()

try:  
    while True :
        speak_jetson()
        respeak()
        
# Crtl + c 누르면 음성 인식 멈춤
except KeyboardInterrupt: 
    pass