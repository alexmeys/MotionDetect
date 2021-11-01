# movement.py
# Using Computer Vision, OpenCV.

import cv2, pandas
from datetime import datetime

# Init objects
first_frame = None
status_list = [None,None]
times= []
df=pandas.DataFrame(columns=["Start", "End"])

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    check, frame = video.read()
    status= 0
    # make the image gray & blurry
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    # restart while loop on first run
    if first_frame is None:
        first_frame=gray
        continue 
    
    delta_frame=cv2.absdiff(first_frame, gray)
    thresh_frame=cv2.threshold(delta_frame, 50, 255, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    (cnts,_)=cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        # 100x100 pixel change
        if cv2.contourArea(contour) < 10000:
            continue
        status=1

        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y),(x+w, y+h), (0,255,0),3)
    
    # Record activity time
    status_list.append(status)

    if status_list[-1] == 1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2]==1:
        times.append(datetime.now())

    #cv2.imshow("Capturing", gray)
    #cv2.imshow("Delta Frame", delta_frame)
    #cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Capturing", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break


# print(status_list)
# print(times)

# put frames start/stop time in DF for time plot (plotting.py)
for i in range(0,len(times),2):
    df=df.append({"Start":times[i], "End":times[i+1]},ignore_index=True)

video.release()
cv2.destroyAllWindows
