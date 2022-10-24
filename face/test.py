
import numpy as np, cv2

import matplotlib.pylab as plt

 

# 크로마키 영상과 합성할 영상 읽기

img1 = cv2.imread("pengsu.png") # 전경

img2 = cv2.imread("startup.png")           # 배경

 

# ROI 선택을 위한 좌표 계산 (가운데에 위치하기 위한)

height1, width1 = img1.shape[:2]

height2, width2 = img2.shape[:2]

x = (width2 - width1) // 2

y = height2 - height1

w = x + width1

h = y + height1

 

# 크로마키 배경 영상에서 크로마키가 있을 법한 영역을 10픽셀 정도로 지정

chromakey = img1[:10, :10, :] # (0,0)~(10,10)까지의 정사각형 좌표

offset = 20 # 임의의 값

 

# 크로마키 영역과 영상 전체를 HSV로 변경

hsv_chroma = cv2.cvtColor(chromakey, cv2.COLOR_BGR2HSV)

hsv_img = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

 

# 크로마키 영역의 H 값에서 offset 만큼 여유를 두어 범위 지정

chroma_h = hsv_chroma[:, :, 0] # 크로마키의 H 값 (초록색 또는 파란색)

lower = np.array([chroma_h.min()-offset, 100, 100]) # 크로마키의 최소 범위

upper = np.array([chroma_h.max()+offset, 255, 255]) # 크로마키의 최대 범위

 

# 마스크 생성 및 마스킹 후 합성

mask = cv2.inRange(hsv_img, lower, upper)   # 사람은 픽셀 0 (검정색)

mask_inv = cv2.bitwise_not(mask)            # 배경은 픽셀 0 (검정색) mask의 반전

roi = img2[y:h, x:w]                        # 배경에서의 관심영역 (가운데)

fg = cv2.bitwise_and(img1, img1, mask=mask_inv) # 사람만 떼내기

bg = cv2.bitwise_and(roi, roi, mask=mask)       # 배경만 떼내기

img2[y:h, x:w] = fg + bg                        # 사람만 + 배경만 (합성)

 

# 결과 출력

# cv2.imshow('chromakey', img1)
#
# cv2.imshow('fg', fg)
#
# cv2.imshow('bg', bg)

cv2.imshow('added', img2)

cv2.waitKey()

cv2.destroyAllWindows()
