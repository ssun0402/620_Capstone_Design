import threading
import cv2

def capture_camera():
    # 캠을 켜기 위한 객체 생성
    cap = cv2.VideoCapture(0)

    # 캠이 켜지는지 확인
    if not cap.isOpened():
        print("캠이 정상적으로 열리지 않았습니다.")
        return

    while True:
        # 프레임 읽기
        ret, frame = cap.read()

        # 프레임이 제대로 읽혔는지 확인
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        # 프레임 화면에 출력
        cv2.imshow('frame', frame)

        # q 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 캠 객체와 창 닫기
    cap.release()
    cv2.destroyAllWindows()

capture_camera()