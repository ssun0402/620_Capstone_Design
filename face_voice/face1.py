import cv2
import face_recognition as fr

def detect_face():
    # 웹캠에서 영상 읽어오기
    cap = cv2.VideoCapture(0)

    while True:
        # 영상 프레임 읽기
        ret, frame = cap.read()

        # BGR 이미지를 RGB 이미지로 변환
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 현재 프레임에서 얼굴 인식
        face_locations = fr.face_locations(rgb_frame)

        # 인식된 얼굴에 박스 그리기
        for face_location in face_locations:
            # 얼굴 위치 정보를 언팩하여 각각의 위치 값 추출
            top, right, bottom, left = face_location

            # 인식된 얼굴 위치에 박스 그리기
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # 영상 출력
        cv2.imshow('Webcam Face Detection', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 작업 완료 후 해제
    cap.release()
    cv2.destroyAllWindows()