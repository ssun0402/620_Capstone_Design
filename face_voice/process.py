from face import capture_camera
from respeak5 import speak_jetson
from respeak5 import respeak
import multiprocessing

if __name__ == '__main__':
    # 프로세스 생성
    p1 = multiprocessing.Process(target = capture_camera)
    p2 = multiprocessing.Process(target = speak_jetson)
    p3 = multiprocessing.Process(target = respeak)

    # 프로세스 실행
    p1.start()
    p2.start()
    p3.start()

    # 프로세스 종료 대기
    p1.join()
    p2.join()
    p3.join()

    print('메인 프로세스 종료')