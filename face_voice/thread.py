import threading
import time
from multi_voice import get_r_name_list
import os
from multi_face import Facerecognition

lock = threading.Lock()

# 스레드 테스트를 위해 def 2개 생성
def func1():
    with lock:
        fr_instance = Facerecognition()
        fr_instance.video()
        time.sleep(1)
        pass

def func2():
    with lock:
        r_name_list = get_r_name_list()
        time.sleep(1)
        pass

def main():
    #스레드 정의
    thread1 = threading.Thread(target=func1)
    thread2 = threading.Thread(target=func2)

    #스레드 시작
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    print("done!")

if __name__ == "__main__":
    main()