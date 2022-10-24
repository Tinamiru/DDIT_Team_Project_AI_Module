import numpy as np
import cv2

xml = 'face.xml'
peng = cv2.imread("4.jpg")
face_cascade = cv2.CascadeClassifier(xml)

cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
cap.set(3,640) # 너비
cap.set(4,480) # 높이

while(True):
    ret, frame = cap.read() 
    frame = cv2.flip(frame, 1) # 좌우 대칭
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.cvtColor(peng, cv2.COLOR_BGR2GRAY)
    
    
    faces = face_cascade.detectMultiScale(gray,1.05,5) 
    #print("Number of faces detected: " + str(len(faces)))

    if len(faces):
        for (x,y,w,h) in faces:
             
            
            face_img = cv2.resize(peng, (w, h), interpolation=cv2.INTER_AREA) # 확대
            
            chromakey = face_img[:10, :10, :] # (0,0)~(10,10)까지의 정사각형 좌표
            
            offset = 20 # 임의의 값
            
            hsv_chroma = cv2.cvtColor(chromakey, cv2.COLOR_BGR2HSV)
            
            hsv_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2HSV)
            
            chroma_h = hsv_chroma[:, :, 0] # 크로마키의 H 값 (초록색 또는 파란색)

            lower = np.array([chroma_h.min()-offset, 100, 100]) # 크로마키의 최소 범위
            
            upper = np.array([chroma_h.max()+offset, 255, 255]) # 크로마키의 최대 범위

            mask = cv2.inRange(hsv_img, lower, upper)   # 사람은 픽셀 0 (검정색)
            
            mask_inv = cv2.bitwise_not(mask)            # 배경은 픽셀 0 (검정색) mask의 반전
            
            roi = frame[y:y+h, x:x+w]                        # 배경에서의 관심영역 (가운데)
            
            fg = cv2.bitwise_and(face_img, face_img, mask=mask_inv) # 사람만 떼내기
            
            bg = cv2.bitwise_and(roi, roi, mask=mask)       # 배경만 떼내기
            
            frame[y:y+h, x:x+w] = fg + bg                        # 사람만 + 배경만 (합성)

            
            
            

   
    cv2.imshow('result', frame)
        
    k = cv2.waitKey(30) & 0xff
    if k == 27: # Esc 키를 누르면 종료
        break

cap.release()
cv2.destroyAllWindows()
