import cv2
import face_recognition as fr
import os
import numpy as np

known_faces_dir = 'C:/Users/gptjs/OneDrive/바탕 화면/GitHub/2023-1-Capstone-/example/webcam/faces'

# 저장된 이미지 파일들을 불러와 얼굴만 추출하여 encoding_list에 추가
def load_known_faces():
    encoding_list = []
    for filename in os.listdir(known_faces_dir):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            image_path = os.path.join(known_faces_dir, filename)
            image = fr.load_image_file(image_path)
            face_encodings = fr.face_encodings(image)[0]
            encoding_list.append(face_encodings)
    return encoding_list

def detect_face():
    # 웹캠에서 영상 읽어오기
    cap = cv2.VideoCapture(0)

    # 저장된 얼굴 이미지들을 불러옴
    known_face_encodings = load_known_faces()

    while True:
        # 영상 프레임 읽기
        ret, frame = cap.read()

        # BGR 이미지를 RGB 이미지로 변환
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 현재 프레임에서 얼굴 인식
        face_locations = fr.face_locations(rgb_frame)
        face_encodings = fr.face_encodings(rgb_frame, face_locations)

        # 인식된 얼굴에 박스 그리기 및 이름 출력
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = fr.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = os.listdir(known_faces_dir)[best_match_index].split('.')[0]
            
            # 인식된 얼굴 위치에 박스 그리기 및 이름 출력
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

        # 영상 출력
        cv2.imshow('Webcam Face Detection', frame)

        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 작업 완료 후 해제
    cap.release()
    cv2.destroyAllWindows()