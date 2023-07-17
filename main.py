import cv2
import sys
import matplotlib.pyplot as plt

img = cv2.imread('image/starry_night.jpg')
# 색깔 이상하게 나온것을 (bgr로 나오는 것을 RGB로 바꿔서 출력해라) 라는 뜻
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
imggrey = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

plt.axis('off')
plt.imshow(imggrey, cmap='gray')
plt.show()
# 창 이름을 적어줘야 실행된다.
# cv2.imshow('Display window',img)
#
# cv2.waitKey()
#
# # 창을 닫는것
# cv2.destroyAllWindows()