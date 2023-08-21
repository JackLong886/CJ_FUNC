import cv2
import numpy as np
prev_point = None
def draw(event, x, y, flags, param):
    global point_list, prev_point, mask
    # 定义绘制颜色（红色）
    color = [0, 0, 255]
    if event == cv2.EVENT_LBUTTONDOWN:
        if prev_point is not None:
            suff_point = (x, y)
            point_list.append(suff_point)
            cv2.line(mask, prev_point, suff_point, color, thickness=7)
            prev_point = suff_point
        else:
            prev_point = (x, y)
            point_list.append(prev_point)


img = cv2.imread(r"C:\Users\DELL\Desktop\xueshan512.png")
mask = np.zeros_like(img)
point_list = []
# 创建窗口并绑定绘图函数
cv2.namedWindow("Mask Drawing")
cv2.setMouseCallback("Mask Drawing", draw)

while True:
    # 显示原始图像和蒙版
    combined = cv2.addWeighted(img, 0.7, mask, 0.3, 0)
    # combined = cv2.add(img, mask)
    cv2.imshow("Mask Drawing", combined)
    # 按ESC键退出
    key = cv2.waitKey(1) & 0xFF
    cv2.waitKey(1) & 0xFF
    if key == 27:
        np.save('points2.npy', point_list)
        break

cv2.waitKey()
cv2.destroyAllWindows()
