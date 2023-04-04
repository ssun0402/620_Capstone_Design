import threading
import time
from multi_voice import get_r_name_list
import os
from multi_face import Facerecognition
# 스레드 테스트를 위해 def 2개 생성
def func1(add):
    face_recognition = Facerecognition()
    time1 = 0
    for names in face_recognition.video() :
        if time1 == 15 :
           time1 += 1
           print(names)

def func2(add):
    r_name_list = get_r_name_list()
    time.sleep(1)

def main():
    #스레드 정의
    thread1 = threading.Thread(target=func2, args=('1',))
    thread2 = threading.Thread(target=func1, args=('2',))

    #스레드 시작
    thread1.start()
    thread2.start()
    print("done!")

    thread1.join()
    thread2.join()
if __name__ == "__main__":
    main()