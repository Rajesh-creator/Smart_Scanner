import urllib.request as req
import numpy as np
import cv2
from PIL import Image
import time
url = " "
while True:
    img = req.urlopen(url)
    img_bytes = bytearray(img.read())
    img_np = np.array(img_bytes, dtype=np.uint8)
    frame = cv2.imdecode(img_np, -1)
    frame_cvt = cv2.cvtcolor(frame, cv2.COLOR_BGR2RGB)
    frame_blur = cv2.GaussianBlur(frame_cvt, (5, 5), 0)
    frame_edge = cv2.Canny(frame_blur, 30, 50)
    contours, h = cv2.findcontours(frame_edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)
        if cv2.contourArea(max_contour) > 5000:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
            object_only = frame[y: y+h, x: x+w]
            cv2.imshow("My Smart Scanner", object_only)
            if cv2.waitkey(1) == ord('s'):
                img_pil = Image.fromarray(object_only)
                time_str = time.strftime('%Y-%m-%d-%H-%M-%S')
                img_pil.save(f"{time_str}.pdf")
                print(time_str)