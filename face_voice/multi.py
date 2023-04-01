import sys
from multiprocessing import Process
from face import detect_face
from voice import speak_jetson

if __name__ == '__main__':
    # Process 객체 생성 및 실행
    p1 = Process(target=detect_face)
    p2 = Process(target=speak_jetson)
    p1.start()
    p2.start()

    # 모든 프로세스가 끝날 때까지 대기
    p1.join()
    p2.join()