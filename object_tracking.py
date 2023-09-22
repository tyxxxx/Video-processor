import cv2
import numpy as np
from object_detection import ObjectDetection
import math

# Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture("test3.mp4")

# Initialize count
count = 0
center_points_prev_frame = []

tracking_objects = {}
track_id = 0

frame_height = np.int0(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_width = np.int0(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#videoWriter = cv2.VideoWriter("foreground_test2.mp4", fourcc, 30, (1920,1080))
rects = []

while True:
    ret, frame = cap.read()
    count += 1
    if not ret:
        break
    #vis = frame.copy()
    vis = np.zeros_like(frame)
    vis[:,:,:] = 255

    # Point current frame
    center_points_cur_frame = []

    # Detect objects on frame
    (class_ids, scores, boxes) = od.detect(frame)
    for i in range(len(boxes)):
        box = boxes[i]
        class_id = class_ids[i]
        (x, y, w, h) = box
        cx = int((x + x + w) / 2)
        cy = int((y + y + h) / 2)
        center_points_cur_frame.append((cx, cy))
        #print("FRAME N°", count, " ", x, y, w, h)

        # cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print("class id is", class_ids)
        if class_id == 0 or class_id == 49:
            print("box is: ",box)
            cv2.imshow("foreground", frame[y:y+h, x:x+w])
            cv2.waitKey()
            for i in range(y, y+h):
                for j in range(x, x+w):
                    vis[i,j] = frame[i,j]
                    #vis[i,j] = [0, 0, 0]
            rects.append([x, y, w, h])

    # write tempory images
    #cv2.imwrite('test2/frame_'+str(count)+'.jpg', vis) 
    #videoWriter.write(vis)
    '''
    if count % 5 == 0:
        cv2.imwrite('images/frame_'+str(count)+'.jpg', vis)    
    '''
    # Only at the beginning we compare previous and current frame
    if count <= 2:
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                if distance < 20:
                    tracking_objects[track_id] = pt
                    track_id += 1
    else:

        tracking_objects_copy = tracking_objects.copy()
        center_points_cur_frame_copy = center_points_cur_frame.copy()

        for object_id, pt2 in tracking_objects_copy.items():
            object_exists = False
            for pt in center_points_cur_frame_copy:
                distance = math.hypot(pt2[0] - pt[0], pt2[1] - pt[1])

                # Update IDs position
                if distance < 20:
                    tracking_objects[object_id] = pt
                    object_exists = True
                    if pt in center_points_cur_frame:
                        center_points_cur_frame.remove(pt)
                    continue

            # Remove IDs lost
            if not object_exists:
                tracking_objects.pop(object_id)

        # Add new IDs found
        for pt in center_points_cur_frame:
            tracking_objects[track_id] = pt
            track_id += 1

    for object_id, pt in tracking_objects.items():
        cv2.circle(frame, pt, 5, (0, 0, 255), -1)
        cv2.putText(frame, str(object_id), (pt[0], pt[1] - 7), 0, 1, (0, 0, 255), 2)

    print("Tracking objects")
    print(tracking_objects)


    print("CUR FRAME LEFT PTS")
    print(center_points_cur_frame)



    #cv2.imshow("Frame", vis)

    # Make a copy of the points
    center_points_prev_frame = center_points_cur_frame.copy()

    key = cv2.waitKey(1)
    if key == 27:
        break
#videoWriter.release()
np.save("rects_test2.npy", rects)
print("len of rects is",len(rects))
cap.release()
cv2.destroyAllWindows()
