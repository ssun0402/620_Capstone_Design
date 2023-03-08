from face import ff
from respeak5 import  re
import multiprocessing

if __name__ == '__main__':
    # 프로세스 생성
    p1 = multiprocessing.Process(target = ff)
    p2 = multiprocessing.Process(target = re)

    # 프로세스 실행
    p1.start()
    p2.start()

    # 프로세스 종료 대기
    p1.join()
    p2.join()

    print('메인 프로세스 종료')